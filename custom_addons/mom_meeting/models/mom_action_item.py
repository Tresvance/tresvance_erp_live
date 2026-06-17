# -*- coding: utf-8 -*-
from odoo import models, fields, api


class MomActionItem(models.Model):
    _name = 'mom.action.item'
    _description = 'Meeting Action Item'
    _order = 'sequence, id'

    meeting_id = fields.Many2one(
        'mom.meeting',
        string='Meeting',
        required=True,
        ondelete='cascade',
    )
    sequence = fields.Integer(default=10)
    description = fields.Char(
        string='Action Item',
        required=True,
    )
    responsible_id = fields.Many2one(
        'res.users',
        string='Responsible',
    )
    deadline = fields.Date(string='Deadline')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'High'),
        ('2', 'Critical'),
    ], string='Priority', default='0')
    state = fields.Selection([
        ('pending', 'Pending'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='pending')
    notes = fields.Text(string='Notes')

    # ── Carried from previous meeting ─────────────────────────────────────────
    carried_over = fields.Boolean(
        string='Carried Over',
        help='Tick if this action was not completed from a previous meeting',
    )
    source_meeting_id = fields.Many2one(
        'mom.meeting',
        string='From Meeting',
        help='Original meeting where this action was raised',
    )
