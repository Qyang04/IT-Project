import pandas as pd
import pickle
from sklearn.metrics import accuracy_score
from sklearn.model_selection import TimeSeriesSplit
from sklearn.feature_selection import SequentialFeatureSelector
from sklearn.linear_model import RidgeClassifier
from sklearn.preprocessing import MinMaxScaler

# Import your custom functions
from predict_functions import add_target, backtest, find_team_average, add_col

def preprocess_and_train():
    df = pd.read_csv("nba_games.csv", index_col=0)
    df = df.sort_values("date")
    df = df.reset_index(drop=True)
    df = df.drop(["mp.1", "mp_opp.1", "index_opp"], axis=1)

    # Add target
    df = df.groupby("team", group_keys=False).apply(add_target)
    df["target"] = df["target"].fillna(2).astype(int)

    # Clear entire empty columns
    nulls = pd.isnull(df)
    nulls = nulls.sum()
    total_rows = df.shape[0]
    nulls = nulls[nulls == total_rows]
    df = df.fillna(0)

    valid_columns = df.columns[~df.columns.isin(nulls.index)]
    df = df[valid_columns].copy()

    # Feature selection and scaling
    removed_columns = ["season", "date", "won", "target", "team", "team_opp"]
    selected_columns = df.columns[~df.columns.isin(removed_columns)]

    scaler = MinMaxScaler()
    df[selected_columns] = scaler.fit_transform(df[selected_columns])

    # Prepare model
    rr = RidgeClassifier(alpha=1)
    split = TimeSeriesSplit(n_splits=3)
    sfs = SequentialFeatureSelector(rr, n_features_to_select=40, direction="forward", cv=split, n_jobs=1)

    # data rolling
    df_rolling = df[list(selected_columns) + ["won", "season"]]
    df_rolling = df_rolling.groupby(["season"], group_keys=False).apply(find_team_average)
    rolling_cols = [f"{col}_5" for col in df_rolling.columns]
    df_rolling.columns = rolling_cols
    df = pd.concat([df, df_rolling], axis=1)

    df = df.dropna()

    df["home_next"] = add_col(df, "home")
    df["team_opp_next"] = add_col(df, "team_opp")
    df["date_next"] = add_col(df, "date")

    full = df.merge(df[rolling_cols + ["team_opp_next", "date_next", "team"]], left_on=["team", "date_next"], right_on=["team_opp_next", "date_next"])
    removed_columns = list(full.columns[full.dtypes == "object"]) + removed_columns
    selected_columns = full.columns[~full.columns.isin(removed_columns)]
    sfs.fit(full[selected_columns], full["target"])
    predictors = list(selected_columns[sfs.get_support()])
    predictions = backtest(full, rr, predictors)
    predictions = predictions[predictions["actual"] != 2]
    accuracy = accuracy_score(predictions['actual'], predictions['prediction'])

    predictions['correct'] = predictions['actual'] == predictions['prediction']
    correct_count = predictions['correct'].sum()
    incorrect_count = len(predictions) - correct_count

    # Get the game details
    game_details = full[['date', 'team_x', 'team_opp']].copy()
    game_details.columns = ['date', 'team', 'team_opp']  # Rename 'team_x' to 'team'

    # Merge predictions with game details
    predictions_with_details = pd.merge(predictions.reset_index(), game_details.reset_index(), left_on='index', right_on='index')
    predictions_with_details = predictions_with_details.drop('index', axis=1)

    # Save processed data and model
    with open('processed_data.pkl', 'wb') as f:
        pickle.dump({
            'predictions_with_details': predictions_with_details,
            'accuracy': accuracy,
            'correct_count': correct_count,
            'incorrect_count': incorrect_count
        }, f)

if __name__ == '__main__':
    preprocess_and_train()