## Initial Setup and Migration
To generate and apply migrations using Alembic, you need to ensure that Alembic is properly set up in your project. Here's a step-by-step guide to set up Alembic and generate the new migration:

### Step 1: Initialize Alembic
Install Alembic:
Ensure Alembic is installed in your virtual environment:

```sh
pip install alembic
```
Initialize Alembic:
Run the following command in your project directory to initialize Alembic:

```sh
alembic init alembic
```
This will create an alembic directory and an alembic.ini file.

### Step 2: Configure Alembic
Edit alembic.ini:
Open alembic.ini and set your database URL. Replace <your_database_url> with your actual database URL:

```ini
sqlalchemy.url = sqlite:///./test.db
```
Edit `alembic/env.py`:
In alembic/env.py, configure the target metadata by editing this part:

```python
...

from app.models import Base  # Import your models
...

# add your model's MetaData object here
# for 'autogenerate' support
target_metadata = Base.metadata
```

### Step 3: Generate a New Migration
Create the Migration Script:
Generate a new migration script that will reflect the changes in your models (e.g., removing the posts relationship from the User model):

```sh
alembic revision --autogenerate -m "Remove posts relationship from User"
```
Edit the Migration Script:
The generated migration script should look like this:

```python
"""Remove posts relationship from User

Revision ID: your_revision_id
Revises: previous_revision_id
Create Date: YYYY-MM-DD HH:MM:SS.SSSSSS

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'your_revision_id'
down_revision = 'previous_revision_id'
branch_labels = None
depends_on = None

def upgrade():
    # No action needed for removing the relationship from the model
    pass

def downgrade():
    # Add back the posts relationship in downgrade if necessary
    pass
```
Since removing the posts relationship from the User model doesn't affect the database schema directly, the upgrade function can be left empty.

### Step 4: Apply the Migration
Apply the Migration:
Run the following command to apply the migration to your database:
```sh
alembic upgrade head
```

### Summary
Initialize Alembic: Run alembic init alembic to set up Alembic.
Configure Alembic: Edit alembic.ini and alembic/env.py to configure Alembic for your project.
Generate a New Migration: Use alembic revision --autogenerate -m "Remove posts relationship from User" to create a new migration script.
Apply the Migration: Run alembic upgrade head to apply the migration to your database.
With these steps, you should be able to set up Alembic, generate the necessary migration, and apply it to update your database schema.

## Add new model
### Step 1. Modify Models:
Ensure your ChatMessage model is added in models.py.

Generate New Migration:

```sh
alembic revision --autogenerate -m "Add ChatMessage model"
```
Review Migration:
Verify the generated script in `alembic/versions`.

Apply Migration:

```sh
alembic upgrade head
```
After completing these steps, your database schema will be updated to include the ChatMessage model, allowing you to store chat messages in the database.