

traditional_investor_stage1 = \
    "SELECT investor, investor_id, invest_amount, invest_change, security_id, isin, issue_date, maturity_date "\
        "FROM "\
            "(SELECT "\
                "report_date, "\
                "investor_holdings.investor_name AS investor,"\
                "investor_id,"\
                "AVG(investor_holdings.amount_held) AS invest_amount,"\
                "AVG(investor_holdings.latest_change) AS invest_change,"\
                "investor_holdings.security_id, "\
                "MAX(isin) as isin,"\
                "MAX(issue_date) as issue_date, "\
                "MAX(maturity_date) as maturity_date "\
            "FROM investor_holdings "\
            "INNER JOIN securities ON investor_holdings.security_id = securities.id "\
            "INNER JOIN issuing_entities ON securities.issuing_entity_id = issuing_entities.id "\
            "INNER JOIN organizations ON issuing_entities.organization_id = organizations.id "\
            "INNER JOIN gics ON organizations.sector = gics.sub_industry_id "\
            "INNER JOIN security_issues ON security_issues.security_id = securities.id "\
            "WHERE investor_holdings.deleted_at is NULL "\
            "AND investor_holdings.report_date > '{}' "\
            "AND issuing_entities.name = '{}' "\
            "AND securities.currency = '{}' "\
            "AND gics.industry_group = '{}' GROUP BY (investor_holdings.investor_name, " \
                "investor_holdings.investor_id, " \
                "investor_holdings.security_id, " \
                "investor_holdings.report_date)) as FOO "


non_traditional_investor_stage1 = \
        "SELECT investor, investor_id, invest_amount, invest_change, security_id, isin, issue_date, maturity_date "\
        "FROM "\
            "(SELECT "\
                "report_date, "\
                "investor_holdings.investor_name AS investor,"\
                "investor_id,"\
                "AVG(investor_holdings.amount_held) AS invest_amount,"\
                "AVG(investor_holdings.latest_change) AS invest_change,"\
                "investor_holdings.security_id, "\
                "MAX(isin) as isin,"\
                "MAX(issue_date) as issue_date, "\
                "MAX(maturity_date) as maturity_date "\
            "FROM investor_holdings "\
            "INNER JOIN securities ON investor_holdings.security_id = securities.id "\
            "INNER JOIN issuing_entities ON securities.issuing_entity_id = issuing_entities.id "\
            "INNER JOIN organizations ON issuing_entities.organization_id = organizations.id "\
            "INNER JOIN gics ON organizations.sector = gics.sub_industry_id "\
            "INNER JOIN security_issues ON security_issues.security_id = securities.id "\
            "WHERE investor_holdings.deleted_at is NULL "\
            "AND investor_holdings.report_date > '{}' "\
            "AND securities.currency = '{}' "\
            "AND gics.industry_group = '{}' GROUP BY "\
            "(investor_holdings.investor_name, " \
                "investor_holdings.investor_id, " \
                "investor_holdings.security_id, " \
                "investor_holdings.report_date)) as FOO "