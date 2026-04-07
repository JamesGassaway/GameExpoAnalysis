import pandas as pd

# Load your data (CSV exported from Google Forms)
df = pd.read_csv("game_expo_responses.csv")

# List of scoring categories
categories = [
    "Gameplay",
    "Creativity",
    "Visual Design",
    "Audio Design",
    "User Experience (UX)",
    "Technical Achievement",
    "Polish"
]

# --------------------------------------------------
# 1. BEST PROJECT IN EACH CATEGORY
# --------------------------------------------------
def best_in_each_category(df):
    print("\n=== Best Project Per Category ===")
    for category in categories:
        avg_scores = df.groupby("Game Title")[category].mean()
        best_game = avg_scores.idxmax()
        best_score = avg_scores.max()
        print(f"{category}: {best_game} ({best_score:.2f})")

# --------------------------------------------------
# 2. OVERALL SCORES (1st, 2nd, 3rd)
# --------------------------------------------------
def overall_scores(df):
    # Compute total score per entry
    df["Total Score"] = df[categories].sum(axis=1)

    # Average total score per game
    overall_scores = df.groupby("Game Title")["Total Score"].mean()

    # Sort descending
    ranked = overall_scores.sort_values(ascending=False)

    print("\n=== Overall Rankings ===")
    print(ranked)

    print("\nTop 5 Games:")
    print(ranked.head(5))

# --------------------------------------------------
# 3. COMMENTS PER PROJECT
# --------------------------------------------------
def comments_per_project(df):
    print("\n=== Comments Per Project ===")

    for game, group in df.groupby("Game Title"):
        print(f"\n--- {game} ---")
        
        positives = group["Best Thing I Liked"].dropna()
        improvements = group["One Suggestion For Improvement"].dropna()
        
        print("\nTop Positive Feedback:")
        print(positives.value_counts().head(3))
        
        print("\nCommon Suggestions:")
        print(improvements.value_counts().head(3))

# --------------------------------------------------
# STANDARD DEVIATION
# --------------------------------------------------
def standard_deviation(df):
    std_dev = df.groupby("Game Title")[categories].std().mean(axis=1)
    return std_dev

# --------------------------------------------------
# 4. CONSISTENCY
# --------------------------------------------------
def consistency(df):
    print("\n=== Score Consistency (Standard Deviation) ===")

    std_dev = standard_deviation(df)

    # Lower = more consistent scores
    print(std_dev.sort_values())

# --------------------------------------------------
# 5. BONUS: MOST POLARIZING GAMES
# --------------------------------------------------
def most_polarizing_games(df):
    std_dev = standard_deviation(df)
    print("\n=== Most Polarizing Games ===")
    print(std_dev.sort_values(ascending=False).head(3))

# --------------------------------------------------
# 6. CATEGORY AVERAGES (Event Insights)
# --------------------------------------------------
def event_insights(df):
    print("\n=== Category Averages Across All Games ===")
    print(df[categories].mean())

# --------------------------------------------------
# 7. PROJECTS BY CATEGORY
# --------------------------------------------------
def top_projects_by_category(df, category, top_n=10):
    """
    Prints the top N projects for a given category based on average score.

    Parameters:
        df (DataFrame): Your data
        category (str): Category name (must match column exactly)
        top_n (int): Number of top projects to display (default = 10)
    """

    # Check if category exists
    if category not in df.columns:
        print(f"Error: '{category}' is not a valid column.")
        print("Available categories:")
        print(df.columns.tolist())
        return

    # Group by game and compute average score for the category
    avg_scores = df.groupby("Game Title")[category].mean()

    # Sort descending and get top N
    top_projects = avg_scores.sort_values(ascending=False).head(top_n)

    print(f"\n=== Top {top_n} Projects for {category} ===")
    for i, (game, score) in enumerate(top_projects.items(), start=1):
        print(f"{i}. {game} — {score:.2f}")

def ask_and_show_top_projects(df):
    category = input("Enter a category: ")
    top_projects_by_category(df, category)

def get_data(df):
    print("Select an option: ")
    print("1: Best Project in Each Category")
    print("2: Overall Scores")
    print("3: Comments Per Project")
    print("4: Standard Deviation")
    print("5: Most Polarizing Games")
    print("6: Expo Insights")
    print("7: Top project in a category")
    category = input("Selection: ")

    match category:
        case "1":
            best_in_each_category(df)
        case "2":
            overall_scores(df)
        case "3":
            comments_per_project(df)
        case "4":
            consistency(df)
        case "5":
            most_polarizing_games(df)
        case "6":
            event_insights(df)
        case "7":
            ask_and_show_top_projects(df)

get_data(df)