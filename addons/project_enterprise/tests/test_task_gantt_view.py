# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import Command
from odoo.fields import Datetime

from odoo.addons.project.models.project_task import CLOSED_STATES
from odoo.addons.project.tests.test_project_base import TestProjectCommon


class TestTaskGanttView(TestProjectCommon):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.user_gantt_test_1, cls.user_gantt_test_2, cls.user_gantt_test_3, cls.user_gantt_test_4 = cls.env['res.users'].with_context({'mail_create_nolog': True}).create([{
            'login': login,
            'name': login,
            'groups_id': [Command.set(cls.env.ref('project.group_project_user').ids)],
        } for login in ('GVU1', 'GVU2', 'GVU3', 'GVU4')])
        cls.project_gantt_test_1, cls.project_gantt_test_2 = cls.env['project.project'].with_context({'mail_create_nolog': True}).create([{
            'name': 'Project Gantt View Test 1',
        }, {
            'name': 'Project Gantt View Test 2',
        }])

    def test_empty_line_tasks(self):
        """This test will check that the group expand method in tasks works properly"""
        self.env['project.task'].with_context({'mail_create_nolog': True}).create([{
            'name': 'Citron',
            'user_ids': user,
            'project_id': project.id,
            'state': state,
            'planned_date_begin': date,
            'date_deadline': date,
        } for user, project, state, date in [
            (self.user_gantt_test_1, self.project_gantt_test_1, '01_in_progress', Datetime.to_datetime('2023-01-01')),
            (self.user_gantt_test_2, self.project_gantt_test_1, '01_in_progress', Datetime.to_datetime('2023-01-25')),
            (self.user_gantt_test_3, self.project_gantt_test_1, '1_done', Datetime.to_datetime('2023-01-25')),
            (self.user_gantt_test_4, self.project_gantt_test_2, '01_in_progress', Datetime.to_datetime('2023-01-25')),
        ]])

        empty_line_projects = [self.env['project.task'].with_context({
            'gantt_start_date': Datetime.to_datetime('2023-01-02'),
            'gantt_scale': 'day',
            'default_project_id': project.id,
        })._group_expand_user_ids(None, [('state', 'not in', list(CLOSED_STATES))], None) for project in [
            self.project_gantt_test_1,
            self.project_gantt_test_2,
        ]]

        self.assertTrue(self.user_gantt_test_1 in empty_line_projects[0], 'There should be an empty line in project 1 for test user 1') # last period
        self.assertTrue(self.user_gantt_test_2 in empty_line_projects[0], 'There should be an empty line in project 1 for test user 2') # future
        self.assertTrue(self.user_gantt_test_3 not in empty_line_projects[0], 'There shouldn\'t be an empty line in project 1 for test user 3') # closed task
        self.assertTrue(self.user_gantt_test_4 not in empty_line_projects[0], 'There shouldn\'t be an empty line in project 1 for test user 4') # different project
        self.assertTrue(self.user_gantt_test_4 in empty_line_projects[1], 'There should be an empty line in project 2 for test user 4') # different project
