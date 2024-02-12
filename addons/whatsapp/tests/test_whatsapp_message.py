# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from freezegun import freeze_time
from unittest.mock import patch

from odoo.addons.whatsapp.tests.common import WhatsAppCommon
from odoo.tests import tagged


@tagged('wa_message')
class WhatsAppMessage(WhatsAppCommon):

    @freeze_time('2023-08-20')
    def test_gc_whatsapp_messages(self):
        WhatsAppMessage = self.env['whatsapp.message']

        create_vals_all = [{
            'body': 'Old Sent Message',
            'create_date': datetime(2023, 8, 1),
            'state': 'sent',
        }, {
            'body': 'Old Received Message',
            'create_date': datetime(2023, 6, 2),
            'state': 'received',
        }, {
            'body': 'Old Failed Message',
            'create_date': datetime(2023, 5, 15),
            'state': 'error',
        }, {
            'body': 'Old Queued Message',
            'create_date': datetime(2023, 4, 7),
            'state': 'outgoing',
        }, {
            'body': 'Recent Sent Message',
            'create_date': datetime(2023, 8, 7),
            'state': 'sent',
        }, {
            'body': 'Recent Received Message',
            'create_date': datetime(2023, 8, 12),
            'state': 'received',
        }, {
            'body': 'Recent Failed Message',
            'create_date': datetime(2023, 8, 19),
            'state': 'error',
        }]
        # individual free_time required as we cannot set create_date anymore
        whatsapp_message_ids = self.env['whatsapp.message']
        for vals in create_vals_all:
            create_date = vals.pop('create_date')
            with patch.object(self.env.cr, 'now', lambda: create_date):
                whatsapp_message_ids += WhatsAppMessage.create(vals)
        [old_sent_message,
         old_received_message,
         old_failed_message,
         old_queued_message,
         recent_sent_message,
         recent_received_message,
         recent_failed_message] = whatsapp_message_ids

        WhatsAppMessage._gc_whatsapp_messages()
        all_messages = WhatsAppMessage.search([])

        for kept_message in [
            old_failed_message, old_queued_message,
            recent_sent_message, recent_received_message, recent_failed_message
        ]:
            self.assertIn(kept_message, all_messages)

        for deleted_message in [old_sent_message, old_received_message]:
            self.assertNotIn(
                deleted_message,
                all_messages
            )
