import sqlite3
import datetime
import click
from rich.console import Console
from rich.table import Table
from rich.markdown import Markdown
from rich import box

class RoadmapTracker:
    def __init__(self, db_path="roadmap.db"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.console = Console()
        self.setup_database()

    def setup_database(self):
        self.cursor.executescript("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                category TEXT,
                description TEXT,
                status TEXT DEFAULT 'pending',
                completion_date TEXT
            );

            CREATE TABLE IF NOT EXISTS progress (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT,
                notes TEXT
            );
        """)
        self.conn.commit()

    def add_initial_tasks(self):
        # All tasks from the roadmap
        tasks = [
            # January
            ('2025-01-19', 'Python', 'Review Pandas, NumPy, and Matplotlib', 'pending'),
            ('2025-01-19', 'Algorithms', 'Start Rabin-Karp Algorithm', 'pending'),
            ('2025-01-20', 'Visualization', 'Learn Seaborn and Plotly', 'pending'),
            ('2025-01-25', 'Algorithms', 'Complete Knuth-Morris-Pratt (KMP) Algorithm', 'pending'),
            ('2025-01-25', 'Project', 'Practice visualization techniques using a dataset', 'pending'),
            
            # January Week 2
            ('2025-01-26', 'Statistics', 'Explore Statsmodels for statistical analysis', 'pending'),
            ('2025-01-26', 'Algorithms', 'Learn Z-Algorithm', 'pending'),
            ('2025-01-27', 'Math', 'Linear algebra basics - vectors and matrices', 'pending'),
            ('2025-02-01', 'Algorithms', 'Complete Manacher\'s Algorithm', 'pending'),
            ('2025-02-01', 'Project', 'Implement matrix operations visualization using Plotly', 'pending'),

            # February Week 1
            ('2025-02-02', 'Algorithms', 'Learn Aho-Corasick Algorithm', 'pending'),
            ('2025-02-02', 'Statistics', 'Practice statistics problems', 'pending'),
            ('2025-02-03', 'Statistics', 'Study descriptive statistics and distributions', 'pending'),
            ('2025-02-08', 'Algorithms', 'Learn Merge Sort and Quick Sort', 'pending'),
            ('2025-02-08', 'Project', 'Practice hypothesis testing with dataset', 'pending'),

            # February Week 2
            ('2025-02-09', 'Algorithms', 'Explore Counting Sort and Radix Sort', 'pending'),
            ('2025-02-09', 'SQL', 'Practice SQL queries on HackerRank', 'pending'),
            ('2025-02-10', 'SQL', 'SQL basics - SELECT, WHERE, JOIN, GROUP BY', 'pending'),
            ('2025-02-10', 'Algorithms', 'Learn DFS and BFS', 'pending'),
            ('2025-02-15', 'Algorithms', 'Learn Dijkstra\'s Algorithm', 'pending'),

            # February Week 3
            ('2025-02-16', 'Algorithms', 'Explore Bellman-Ford Algorithm', 'pending'),
            ('2025-02-17', 'ML', 'Study Linear Regression and Logistic Regression', 'pending'),
            ('2025-02-17', 'Algorithms', 'Learn Floyd-Warshall and Topological Sort', 'pending'),
            ('2025-02-22', 'Algorithms', 'Learn Prim\'s and Kruskal\'s Algorithms', 'pending'),
            ('2025-02-22', 'Project', 'Build ML basics mini-project', 'pending'),

            # February Week 4
            ('2025-02-23', 'Algorithms', 'Learn Tarjan\'s and Kosaraju\'s Algorithms', 'pending'),
            ('2025-02-24', 'ML', 'Study K-Means Clustering and PCA', 'pending'),
            ('2025-02-24', 'Algorithms', 'Learn Suffix Array and LCP Array', 'pending'),
            ('2025-02-29', 'Project', 'Implement K-Means clustering project', 'pending'),
            ('2025-02-29', 'Algorithms', 'Learn Trie data structure', 'pending'),

            # March Week 1
            ('2025-03-01', 'Review', 'Review February topics', 'pending'),
            ('2025-03-02', 'DSA', 'Focus on Graph and Dynamic Programming', 'pending'),
            ('2025-03-07', 'Algorithms', 'Learn Edmonds-Karp and Dinic\'s Algorithms', 'pending'),

            # March Week 2
            ('2025-03-08', 'Review', 'Revise graph algorithms', 'pending'),
            ('2025-03-09', 'Big Data', 'Learn PySpark basics - RDDs and DataFrames', 'pending'),
            ('2025-03-09', 'Algorithms', 'Study Ternary and Exponential Search', 'pending'),
            ('2025-03-14', 'Algorithms', 'Complete Bucket Sort', 'pending'),
            ('2025-03-14', 'Project', 'Analyze large dataset using PySpark', 'pending'),

            # March Week 3
            ('2025-03-15', 'Cloud', 'Build cloud-based data pipeline project', 'pending'),
            ('2025-03-15', 'Algorithms', 'Learn Rotating Calipers', 'pending'),
            ('2025-03-16', 'Cloud', 'Learn AWS basics or Google Cloud', 'pending'),
            ('2025-03-16', 'Algorithms', 'Study Convex Hull and Closest Pair', 'pending'),

            # March Week 4
            ('2025-03-22', 'Review', 'Review March progress', 'pending'),
            ('2025-03-23', 'Project', 'Build PySpark project with large dataset', 'pending'),
            ('2025-03-23', 'Algorithms', 'Practice backtracking problems', 'pending'),
            ('2025-03-28', 'Project', 'Finalize PySpark project', 'pending'),

            # April Week 1
            ('2025-04-01', 'Review', 'Revise ML concepts', 'pending'),
            ('2025-04-02', 'Deep Learning', 'Learn TensorFlow/PyTorch basics', 'pending'),
            ('2025-04-02', 'Project', 'Build binary classification neural network', 'pending'),
            ('2025-04-07', 'Deep Learning', 'Explore CNNs and RNNs', 'pending'),

            # April Week 2
            ('2025-04-08', 'Review', 'Revise ETL basics', 'pending'),
            ('2025-04-09', 'Data Engineering', 'Learn Apache Airflow and ETL', 'pending'),
            ('2025-04-09', 'Project', 'Build basic ETL pipeline', 'pending'),
            ('2025-04-14', 'Practice', 'Practice data engineering tasks', 'pending'),

            # April Week 3
            ('2025-04-15', 'Project', 'Explore Kaggle datasets', 'pending'),
            ('2025-04-16', 'Deep Learning', 'Implement CNN for image classification', 'pending'),
            ('2025-04-16', 'Project', 'Participate in Kaggle challenges', 'pending'),
            ('2025-04-21', 'Project', 'Build collaborative Kaggle project', 'pending'),

            # April Week 4
            ('2025-04-22', 'Review', 'Catch up and final review', 'pending'),
            ('2025-04-23', 'Review', 'Revise algorithms and ML concepts', 'pending'),
            ('2025-04-23', 'Project', 'Build final presentation', 'pending'),
            ('2025-04-28', 'Portfolio', 'Polish GitHub repository and portfolio', 'pending'),
        ]
        
        self.cursor.executemany(
            "INSERT OR IGNORE INTO tasks (date, category, description, status) VALUES (?, ?, ?, ?)",
            tasks
        )
        self.conn.commit()

    def view_tasks(self, days=7):
        table = Table(title=f"Upcoming Tasks (Next {days} days)", box=box.ROUNDED)
        table.add_column("ID", style="blue")
        table.add_column("Date", style="cyan")
        table.add_column("Category", style="magenta")
        table.add_column("Task", style="green")
        table.add_column("Status", style="yellow")

        today = datetime.datetime.now()
        end_date = today + datetime.timedelta(days=days)

        self.cursor.execute("""
            SELECT id, date, category, description, status 
            FROM tasks 
            WHERE date BETWEEN ? AND ?
            ORDER BY date
        """, (today.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')))
        
        for row in self.cursor.fetchall():
            table.add_row(str(row[0]), row[1], row[2], row[3], row[4])

        self.console.print(table)

    def view_by_category(self, category):
        table = Table(title=f"Tasks for Category: {category}", box=box.ROUNDED)
        table.add_column("ID", style="blue")
        table.add_column("Date", style="cyan")
        table.add_column("Task", style="green")
        table.add_column("Status", style="yellow")

        self.cursor.execute("""
            SELECT id, date, description, status 
            FROM tasks 
            WHERE category = ?
            ORDER BY date
        """, (category,))
        
        for row in self.cursor.fetchall():
            table.add_row(str(row[0]), row[1], row[2], row[3])

        self.console.print(table)

    def mark_complete(self, task_id):
        completion_date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute(
            "UPDATE tasks SET status = 'completed', completion_date = ? WHERE id = ?",
            (completion_date, task_id)
        )
        self.conn.commit()

    def add_progress_note(self, note):
        date = datetime.datetime.now().strftime('%Y-%m-%d')
        self.cursor.execute(
            "INSERT INTO progress (date, notes) VALUES (?, ?)",
            (date, note)
        )
        self.conn.commit()

    def view_progress(self):
        table = Table(title="Progress Notes", box=box.ROUNDED)
        table.add_column("Date", style="cyan")
        table.add_column("Notes", style="green", wrap=True)

        self.cursor.execute("SELECT date, notes FROM progress ORDER BY date DESC")
        for row in self.cursor.fetchall():
            table.add_row(row[0], row[1])

        self.console.print(table)

    def get_categories(self):
        self.cursor.execute("SELECT DISTINCT category FROM tasks ORDER BY category")
        return [row[0] for row in self.cursor.fetchall()]

@click.group()
def cli():
    """Learning Roadmap Tracker CLI"""
    pass

@cli.command()
@click.option('--days', default=7, help='Number of days to view')
def tasks(days):
    """View upcoming tasks"""
    tracker = RoadmapTracker()
    tracker.view_tasks(days)

@cli.command()
@click.argument('category')
def by_category(category):
    """View tasks by category"""
    tracker = RoadmapTracker()
    tracker.view_by_category(category)

@cli.command()
def categories():
    """List all available categories"""
    tracker = RoadmapTracker()
    cats = tracker.get_categories()
    console = Console()
    console.print("\nAvailable Categories:", style="bold cyan")
    for cat in cats:
        console.print(f"- {cat}")

@cli.command()
@click.argument('task_id')
def complete(task_id):
    """Mark a task as complete"""
    tracker = RoadmapTracker()
    tracker.mark_complete(task_id)
    click.echo(f"Task {task_id} marked as complete!")

@cli.command()
@click.argument('note')
def add_note(note):
    """Add a progress note"""
    tracker = RoadmapTracker()
    tracker.add_progress_note(note)
    click.echo("Progress note added!")

@cli.command()
def progress():
    """View progress notes"""
    tracker = RoadmapTracker()
    tracker.view_progress()

@cli.command()
def initialize():
    """Initialize the database with initial tasks"""
    tracker = RoadmapTracker()
    tracker.add_initial_tasks()
    click.echo("Database initialized with tasks!")

if __name__ == '__main__':
    cli()