from flask import jsonify
from pgadmin.utils.ajax import make_json_response
from pgadmin.model import db, Database

def get_tables(database):
    """Fetch available tables in a given database."""
    try:
        db_conn = Database.query.filter_by(name=database).first()
        if not db_conn:
            return make_json_response(
                status=404, success=0, info="Database not found."
            )
        
        # Fetch table names using PostgreSQL system catalog
        sql = "SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname = 'public';"
        connection = db_conn.connection()
        cursor = connection.execute(sql)
        tables = [row[0] for row in cursor.fetchall()]

        return jsonify({'tables': tables})

    except Exception as e:
        return make_json_response(status=500, success=0, info=str(e))
