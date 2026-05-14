from django.db import migrations


class Migration(migrations.Migration):
    """
    Custom Migration class that lets you migrate an app other than the one
    you're in.

    Via: http://stackoverflow.com/a/27450550/373243
    """

    migrated_app = None

    def __init__(self, name, app_label):
        super(Migration,self).__init__(name, app_label)
        if self.migrated_app is None:
            self.migrated_app = self.app_label

    def mutate_state(self, project_state, **kwargs):
        new_state = project_state.clone()
        for operation in self.operations:
            operation.state_forwards(self.migrated_app, new_state)
        return new_state

    def apply(self, project_state, schema_editor, collect_sql=False):
        for operation in self.operations:
            if collect_sql and not operation.reduces_to_sql:
                schema_editor.collected_sql.append("--")
                schema_editor.collected_sql.append("-- MIGRATION NOW PERFORMS OPERATION THAT CANNOT BE WRITTEN AS SQL:")
                schema_editor.collected_sql.append("-- %s" % operation.describe())
                schema_editor.collected_sql.append("--")
                continue
            new_state = project_state.clone()
            operation.state_forwards(self.migrated_app, new_state)
            if not schema_editor.connection.features.can_rollback_ddl and operation.atomic:
                with atomic(schema_editor.connection.alias):
                    operation.database_forwards(self.migrated_app, schema_editor, project_state, new_state)
            else:
                operation.database_forwards(self.migrated_app, schema_editor, project_state, new_state)
            project_state = new_state
        return project_state

    def unapply(self, project_state, schema_editor, collect_sql=False):
        to_run = []
        new_state = project_state
        for operation in self.operations:
            if not operation.reversible:
                raise Migration.IrreversibleError("Operation %s in %s is not reversible" % (operation, self))
            new_state = new_state.clone()
            old_state = new_state.clone()
            operation.state_forwards(self.migrated_app, new_state)
            to_run.insert(0, (operation, old_state, new_state))

        for operation, to_state, from_state in to_run:
            if collect_sql:
                if not operation.reduces_to_sql:
                    schema_editor.collected_sql.append("--")
                    schema_editor.collected_sql.append("-- MIGRATION NOW PERFORMS OPERATION THAT CANNOT BE "
                                                       "WRITTEN AS SQL:")
                    schema_editor.collected_sql.append("-- %s" % operation.describe())
                    schema_editor.collected_sql.append("--")
                    continue
            if not schema_editor.connection.features.can_rollback_ddl and operation.atomic:
                with atomic(schema_editor.connection.alias):
                    operation.database_backwards(self.migrated_app, schema_editor, from_state, to_state)
            else:
                operation.database_backwards(self.migrated_app, schema_editor, from_state, to_state)

        return project_state
