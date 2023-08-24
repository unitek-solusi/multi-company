import logging

from odoo import SUPERUSER_ID, api

_logger = logging.getLogger(__name__)

try:
    from odoo.addons.base_multi_company import hooks
except ImportError:
    _logger.info("Cannot find `base_multi_company` module in addons path.")


def post_init_hook(cr, registry):
    #hooks.post_init_hook(
    #    cr,
    #    "base.res_partner_rule",
    #    "res.partner",
    #)

    rule = env.ref(rule_ref)
    if not rule:  # safeguard if it's deleted
        return
    rule.write(
        {
            "active": True,
            "domain_force": (
                "['|', '|', ('no_company_ids', '=', True), ('company_ids', "
                "'in', company_ids), ('user_ids', '!=', False)]"
            ),
        }
    )


def uninstall_hook(cr, registry):
    """Restore product rule to base value.

    Args:
        cr (Cursor): Database cursor to use for operation.
        rule_ref (string): XML ID of security rule to remove the
            `domain_force` from.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    # Change access rule
    rule = env.ref("base.res_partner_rule")
    rule.write(
        {
            "active": False,
            "domain_force": (
                "['|','|',('company_id.child_ids','child_of',"
                "[user.company_id.id]),('company_id','child_of',"
                "[user.company_id.id]),('company_id','=',False)]"
            ),
        }
    )
