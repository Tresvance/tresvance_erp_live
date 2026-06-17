# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MomMeeting(models.Model):
    _name = 'mom.meeting'
    _description = 'Minutes of Meeting'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'meeting_date desc, id desc'

    # ── Basic Info ──────────────────────────────────────────────────────────
    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        default='New',
        tracking=True,
    )
    meeting_title = fields.Char(
        string='Meeting Title',
        required=True,
        tracking=True,
    )
    meeting_date = fields.Date(
        string='Meeting Date',
        required=True,
        default=fields.Date.today,
        tracking=True,
    )
    meeting_time = fields.Float(
        string='Meeting Time',
        help='Time in 24h format (e.g. 14.5 = 2:30 PM)',
    )
    meeting_duration = fields.Float(
        string='Duration (hrs)',
    )
    location = fields.Char(
        string='Location / Platform',
        help='e.g. Office, Google Meet, Zoom, Teams',
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft', tracking=True, required=True)

    # ── Client & Project ─────────────────────────────────────────────────────
    client_id = fields.Many2one(
        'res.partner',
        string='Client',
        required=True,
        domain=[('is_company', '=', True)],
        tracking=True,
    )
    client_contact_id = fields.Many2one(
        'res.partner',
        string='Client Contact Person',
        domain="[('parent_id','=',client_id)]",
    )
    client_email = fields.Char(
        string='Client Email',
        related='client_contact_id.email',
        readonly=True,
    )
    client_phone = fields.Char(
        string='Client Phone',
        related='client_contact_id.phone',
        readonly=True,
    )
    project_id = fields.Many2one(
        'project.project',
        string='Project',
        tracking=True,
    )
    project_type = fields.Selection([
        ('web', 'Web Development'),
        ('erp', 'ERP Implementation'),
        ('mobile', 'Mobile App'),
        ('custom', 'Custom Software'),
        ('maintenance', 'Maintenance & Support'),
        ('other', 'Other'),
    ], string='Project Type', tracking=True)

    # ── Participants ──────────────────────────────────────────────────────────
    participant_ids = fields.Many2many(
        'res.users',
        'mom_meeting_participant_rel',
        'meeting_id',
        'user_id',
        string='Internal Participants (Our Team)',
    )
    client_participant_ids = fields.Many2many(
        'res.partner',
        'mom_meeting_client_participant_rel',
        'meeting_id',
        'partner_id',
        string='Client Participants',
        domain="[('parent_id','=',client_id)]",
    )
    chaired_by = fields.Many2one(
        'res.users',
        string='Meeting Chaired By',
        default=lambda self: self.env.user,
    )
    prepared_by = fields.Many2one(
        'res.users',
        string='MOM Prepared By',
        default=lambda self: self.env.user,
    )

    # ── Meeting Content ───────────────────────────────────────────────────────
    agenda = fields.Html(
        string='Agenda',
        help='Topics planned to be discussed',
    )
    requirements_discussed = fields.Html(
        string='Requirements / Discussion Points',
        help='New requirements or feature requests raised by the client',
    )
    project_update_notes = fields.Html(
        string='Project Status Update Notes',
        help='Current progress, milestones, deliverables discussed',
    )
    decisions_made = fields.Html(
        string='Decisions Made',
    )
    next_meeting_date = fields.Date(
        string='Next Meeting Date',
    )
    next_meeting_agenda = fields.Text(
        string='Next Meeting Agenda',
    )
    general_notes = fields.Html(
        string='Additional Notes / Remarks',
    )

    # ── Action Items (O2M) ────────────────────────────────────────────────────
    action_item_ids = fields.One2many(
        'mom.action.item',
        'meeting_id',
        string='Action Items',
    )
    action_item_count = fields.Integer(
        string='Action Items',
        compute='_compute_action_item_count',
    )

    # ── Computed ──────────────────────────────────────────────────────────────
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        default=lambda self: self.env.company,
    )

    @api.depends('action_item_ids')
    def _compute_action_item_count(self):
        for rec in self:
            rec.action_item_count = len(rec.action_item_ids)

    # ── Sequence ──────────────────────────────────────────────────────────────
    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', 'New') == 'New':
                vals['name'] = self.env['ir.sequence'].next_by_code('mom.meeting') or 'New'
        return super().create(vals_list)

    # ── State transitions ─────────────────────────────────────────────────────
    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_reset_draft(self):
        self.write({'state': 'draft'})

    def action_print_report(self):
        return self.env.ref('mom_meeting.action_report_mom_meeting').report_action(self)

    def _display_name_fields(self):
        return ['name', 'meeting_title']

    def _name_get_fields(self):
        return ['name', 'meeting_title']
