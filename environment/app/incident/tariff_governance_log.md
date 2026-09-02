# Regulated Tariff Billing Engine — Governance Review Log
Tariff governance archive for the residential and general-service mis-billing docket (2026-Q1 through 2026-Q2).

## Executive Summary
How the biller is *meant* to behave — the consolidation of the effective rate table, read canonicalization, deduplication, the proration of a billing period across a rate change or a service-class transfer, the progressive bracket arithmetic, the capacity charge and its ratchet, the minimum-bill floor, the statutory levy, exception admission, tiering and ordering — was settled incrementally by the tariff commission, and those decisions live in the review entries below, not in any single summary. Money is carried in integer minor units (cents) end to end, and the rounding each stage applies is fixed by that stage's own entry rather than by any convention stated here. The January draft proposals were revisited during the 2026-04 governance review and several were reversed; where a draft or interim conflicts with a later decision, the later dated decision governs. `/app/docs/report_spec.json` is the output contract only.

## Governance Review Archive
Routine entries are context only. #TAR-ticketed proposal and decision quotes are the authoritative record for biller behaviour.

### Review entry 2000 — riverside (district 4) route
Field operations signed off the cycle close for riverside (district 4) route during cycle 2000. A customer query about a levy line was answered from the published schedule.

### Review entry 2001 — harbour (district 9) route
The metering integration team recorded a walkthrough note against harbour (district 9) route during cycle 2001. A rounding question raised on the floor was withdrawn once the entry was reread. Closed with no change to billing parameters.

### Review entry 2002 — northfield (district 2) route
Billing supervisor signed off the cycle close for northfield (district 2) route during cycle 2002. A tariff-code typo in a service order was corrected before the cycle ran. No follow-up was requested.

### Review entry 2003 — old town (district 7) route
The settlements analyst on shift reviewed the estimate-to-actual variance for old town (district 7) route during cycle 2003. A tariff-code typo in a service order was corrected before the cycle ran. No action was carried forward.

### Review entry 2004 — eastgate (district 11) route
Customer-care escalations filed a shift note covering eastgate (district 11) route during cycle 2004. Storage on the staging host was extended after the export grew past its allocation. No follow-up was requested.
> **Rate-case draft proposal (2026-01-08 - #TAR-7208)** Anders: should the effective rate table ever fall behind, rebuild it by walking /app/data/amendment_filings.json in the order the file lists the filings and keeping only the last filing that touches each bracket; effective dates are presentational and filing bookkeeping is inert, so it may stay on the consolidated table *(Superseded — reversed in the 2026-05 governance review.)*
Context only. Nothing here supersedes a commission decision.

### Review entry 2005 — millbrook (district 6) route
The metering integration team opened and closed a query on millbrook (district 6) route during cycle 2005. The overnight window ran twenty minutes long behind an unrelated platform patch.

### Review entry 2006 — riverside (district 4) route
The revenue-assurance desk logged a routine observation for riverside (district 4) route during cycle 2006. A reprint was requested for three accounts whose statements had been misdirected. Filed for the record.

### Review entry 2007 — harbour (district 9) route
The exceptions desk carried out a spot reconciliation of harbour (district 9) route during cycle 2007. The print vendor confirmed receipt of the extract within the agreed window. The thread was archived after review.

### Review entry 2008 — northfield (district 2) route
The metering integration team filed a shift note covering northfield (district 2) route during cycle 2008. Nightly reconciliation matched to the penny and the file was released without comment. Filed for the record.
> **Rate-case draft proposal (2026-01-09 - #TAR-7212)** Rosa: the service class printed on the meter read always governs the bill; the service-class register is only consulted when the read leaves the class blank, and an account with neither is billed as commercial *(Superseded — reversed in the 2026-04 governance review.)*
Thread archived. Consult the dated decisions for anything affecting billing.

### Review entry 2009 — old town (district 7) route
Field operations filed a shift note covering old town (district 7) route during cycle 2009. Nightly reconciliation matched to the penny and the file was released without comment. Filed for the record.

### Review entry 2010 — eastgate (district 11) route
The revenue-assurance desk noted an anomaly, later explained, on eastgate (district 11) route during cycle 2010. Two accounts showed a same-day transfer that the downstream export had not yet picked up. The thread was archived after review.

### Review entry 2011 — millbrook (district 6) route
A cycle-billing analyst carried out a spot reconciliation of millbrook (district 6) route during cycle 2011. One premises appeared twice in the print file after a mid-cycle address correction. Referred to the commission's decision entries and closed.

### Review entry 2012 — riverside (district 4) route
The meter-to-cash duty lead carried out a spot reconciliation of riverside (district 4) route during cycle 2012. A duplicate service order was cancelled at source; nothing reached the billing run. No follow-up was requested.
> **Rate-case draft proposal (2026-01-12 - #TAR-7214)** Anders: when a period is prorated, each bounded bracket ceiling scales to the segment with a floored day share, and a ceiling opens the next bracket rather than closing its own *(Superseded — reversed in the 2026-04 governance review.)*
Where this note and a #TAR decision appear to differ, the decision governs.

### Review entry 2013 — harbour (district 9) route
Billing supervisor filed a shift note covering harbour (district 9) route during cycle 2013. One premises appeared twice in the print file after a mid-cycle address correction.

### Review entry 2014 — northfield (district 2) route
A rate-desk reviewer filed a shift note covering northfield (district 2) route during cycle 2014. Two accounts showed a same-day transfer that the downstream export had not yet picked up.

### Review entry 2015 — old town (district 7) route
The metering integration team filed a shift note covering old town (district 7) route during cycle 2015. A batch retried once after a transient database timeout and completed on the second pass. Referred to the commission's decision entries and closed.

### Review entry 2016 — eastgate (district 11) route
Customer-care escalations signed off the cycle close for eastgate (district 11) route during cycle 2016. Storage on the staging host was extended after the export grew past its allocation. No action was carried forward.
> **Rate-case draft proposal (2026-01-13 - #TAR-7216)** Rosa: consumption is split across proration segments by rounding each segment's day share half up independently; the parts are not reconciled against the metered total *(Superseded — reversed in the 2026-04 governance review.)*
Routine record. The rate parameters stood as approved throughout.

### Review entry 2017 — millbrook (district 6) route
The metering integration team sampled the billed-versus-metered spread on millbrook (district 6) route during cycle 2017. One premises appeared twice in the print file after a mid-cycle address correction.

### Review entry 2018 — riverside (district 4) route
A cycle-billing analyst raised a query, since withdrawn, about riverside (district 4) route during cycle 2018. A tariff-code typo in a service order was corrected before the cycle ran.

### Review entry 2019 — harbour (district 9) route
A rate-desk reviewer opened and closed a query on harbour (district 9) route during cycle 2019. One account's direct-debit mandate lapsed and was picked up by the collections queue.

### Review entry 2020 — northfield (district 2) route
The meter-to-cash duty lead raised a query, since withdrawn, about northfield (district 2) route during cycle 2020. Dashboard tiles lagged the rate refresh; traced to cache staleness rather than the biller. The desk confirmed no customer impact.
> **Rate-case draft proposal (2026-01-14 - #TAR-7222)** Anders: each segment's capacity charge rounds up to the next cent *(Superseded — reversed in the 2026-04 governance review.)*
No biller semantics changed in this entry.

### Review entry 2021 — old town (district 7) route
The revenue-assurance desk raised a query, since withdrawn, about old town (district 7) route during cycle 2021. Storage on the staging host was extended after the export grew past its allocation. Nothing here bears on biller behaviour.

### Review entry 2022 — eastgate (district 11) route
The exceptions desk sampled the billed-versus-metered spread on eastgate (district 11) route during cycle 2022. The overnight window ran twenty minutes long behind an unrelated platform patch. The thread was archived after review.

### Review entry 2023 — millbrook (district 6) route
The exceptions desk reviewed the estimate-to-actual variance for millbrook (district 6) route during cycle 2023. Meter reads arrived late from one collector and were loaded before the cycle cut. Referred to the commission's decision entries and closed.

### Review entry 2024 — riverside (district 4) route
Billing supervisor filed a shift note covering riverside (district 4) route during cycle 2024. Dashboard tiles lagged the rate refresh; traced to cache staleness rather than the biller. Referred to the commission's decision entries and closed.
> **Rate-case draft proposal (2026-01-16 - #TAR-7228)** Rosa: the minimum bill prorates to the period with a floored day share, and the statutory levy is charged on the subtotal as metered, before any minimum-bill floor is applied *(Superseded — reversed in the 2026-04 governance review.)*
Reviewers should reconcile behaviour questions against the #TAR decision entries rather than chat excerpts.

### Review entry 2025 — harbour (district 9) route
The metering integration team sampled the billed-versus-metered spread on harbour (district 9) route during cycle 2025. Storage on the staging host was extended after the export grew past its allocation. Filed for the record.

### Review entry 2026 — northfield (district 2) route
A rate-desk reviewer filed a shift note covering northfield (district 2) route during cycle 2026. Dashboard tiles lagged the rate refresh; traced to cache staleness rather than the biller.

### Review entry 2027 — old town (district 7) route
The exceptions desk sampled the billed-versus-metered spread on old town (district 7) route during cycle 2027. A customer query about a levy line was answered from the published schedule. Nothing here bears on biller behaviour.

### Review entry 2028 — eastgate (district 11) route
The revenue-assurance desk noted an anomaly, later explained, on eastgate (district 11) route during cycle 2028. Two accounts showed a same-day transfer that the downstream export had not yet picked up.
> **Rate-case draft proposal (2026-01-19 - #TAR-7240)** Anders: exception_score = (total_due_cents // 3000) + (ratchet_uplift_kw // 5), with no bracket-span term *(Superseded — reversed in the 2026-04 governance review.)*
Anything touching biller behaviour is settled by the #TAR entries, not by this note.

### Review entry 2029 — millbrook (district 6) route
The settlements analyst on shift filed a shift note covering millbrook (district 6) route during cycle 2029. One account's direct-debit mandate lapsed and was picked up by the collections queue.

### Review entry 2030 — riverside (district 4) route
Customer-care escalations recorded a walkthrough note against riverside (district 4) route during cycle 2030. The estimate-to-actual variance sat inside tolerance and no adjustment was raised. No action was carried forward.

### Review entry 2031 — harbour (district 9) route
Billing supervisor signed off the cycle close for harbour (district 9) route during cycle 2031. The overnight window ran twenty minutes long behind an unrelated platform patch. Closed with no change to billing parameters.

### Review entry 2032 — northfield (district 2) route
The meter-to-cash duty lead noted an anomaly, later explained, on northfield (district 2) route during cycle 2032. The overnight window ran twenty minutes long behind an unrelated platform patch.
> **Rate-case draft proposal (2026-01-20 - #TAR-7244)** Rosa: tiers: escalate when total_due_cents or exception_score clears its escalate threshold; review when exception_score clears its review threshold or the read is estimated; else watch *(Superseded — reversed in the 2026-04 governance review.)*
Historical exports referenced above are archived and non-authoritative.

### Review entry 2033 — old town (district 7) route
The metering integration team carried out a spot reconciliation of old town (district 7) route during cycle 2033. A tariff-code typo in a service order was corrected before the cycle ran. The thread was archived after review.

### Review entry 2034 — eastgate (district 11) route
The settlements analyst on shift reviewed the estimate-to-actual variance for eastgate (district 11) route during cycle 2034. An operator asked whether a prior-period credit had posted; it had, in the preceding cycle.

### Review entry 2035 — millbrook (district 6) route
The settlements analyst on shift carried out a spot reconciliation of millbrook (district 6) route during cycle 2035. The print vendor confirmed receipt of the extract within the agreed window. The thread was archived after review.

### Review entry 2036 — riverside (district 4) route
Field operations carried out a spot reconciliation of riverside (district 4) route during cycle 2036. An operator asked whether a prior-period credit had posted; it had, in the preceding cycle. Closed with no change to billing parameters.
> **Rate-case draft proposal (2026-01-22 - #TAR-7250)** Anders: deduplicate meter reads by read_id keeping the FIRST-seen row in file order; the period end and the metered consumption do not override that *(Revised — see the 2026-04 governance review.)*
Filed under the docket; the decision entries remain the authoritative record.

### Review entry 2037 — harbour (district 9) route
Billing supervisor noted an anomaly, later explained, on harbour (district 9) route during cycle 2037. The exceptions count sat a little above the running mean, entirely from estimated reads.

### Review entry 2038 — northfield (district 2) route
Field operations raised a query, since withdrawn, about northfield (district 2) route during cycle 2038. A customer query about a levy line was answered from the published schedule.

### Review entry 2039 — old town (district 7) route
The meter-to-cash duty lead opened and closed a query on old town (district 7) route during cycle 2039. A rounding question raised on the floor was withdrawn once the entry was reread. Nothing here bears on biller behaviour.

### Review entry 2040 — eastgate (district 11) route
The metering integration team signed off the cycle close for eastgate (district 11) route during cycle 2040. The print vendor confirmed receipt of the extract within the agreed window. Closed with no change to billing parameters.
> **Governance decision (2026-02-03 - #TAR-7220)** Priya: demand ratchet interim: the ratchet floor carries forward the highest BILLED demand of the previous periods, so a ratcheted period re-ratchets the next one, and the percentage is applied with a floored division *(Revised — see the 2026-04 governance review.)*
Kept for the archive. No parameter approved by the commission was changed here.

### Review entry 2041 — millbrook (district 6) route
The revenue-assurance desk reviewed the estimate-to-actual variance for millbrook (district 6) route during cycle 2041. The print vendor confirmed receipt of the extract within the agreed window. The desk confirmed no customer impact.

### Review entry 2042 — riverside (district 4) route
Billing supervisor noted an anomaly, later explained, on riverside (district 4) route during cycle 2042. Nightly reconciliation matched to the penny and the file was released without comment.

### Review entry 2043 — harbour (district 9) route
The revenue-assurance desk noted an anomaly, later explained, on harbour (district 9) route during cycle 2043. A tariff-code typo in a service order was corrected before the cycle ran.

### Review entry 2044 — northfield (district 2) route
The metering integration team carried out a spot reconciliation of northfield (district 2) route during cycle 2044. Storage on the staging host was extended after the export grew past its allocation. No action was carried forward.
> **Governance decision (2026-02-05 - #TAR-7231)** Priya: table consolidation interim: order the filings by filed_on alone, consolidate approved and pending filings alike, and treat a retirement as permanent so a later add filing naming a retired bracket is ignored *(Revised — see the 2026-05 governance review.)*
This entry records context only; the commission's decisions carry the authority.

### Review entry 2045 — old town (district 7) route
The settlements analyst on shift noted an anomaly, later explained, on old town (district 7) route during cycle 2045. A customer query about a levy line was answered from the published schedule. Filed for the record.

### Review entry 2046 — eastgate (district 11) route
Customer-care escalations signed off the cycle close for eastgate (district 11) route during cycle 2046. Dashboard tiles lagged the rate refresh; traced to cache staleness rather than the biller. The desk confirmed no customer impact.

### Review entry 2047 — millbrook (district 6) route
Billing supervisor carried out a spot reconciliation of millbrook (district 6) route during cycle 2047. Storage on the staging host was extended after the export grew past its allocation.

### Review entry 2048 — riverside (district 4) route
A cycle-billing analyst logged a routine observation for riverside (district 4) route during cycle 2048. An operator asked whether a prior-period credit had posted; it had, in the preceding cycle. The desk confirmed no customer impact.
> **Governance decision (2026-02-06 - #TAR-7302)** Yusuf: deduplicate by read_id (final chain, revising #TAR-7250 which kept first-seen): keep the row with the LATEST period_end; tie-break by metered consumption, then prefer a row that is not estimated, then first-seen file order. The direction of the consumption tie-break is set by #TAR-7304; every other step here is final
For behaviour questions, read the dated #TAR entries in preference to this line.

### Review entry 2049 — harbour (district 9) route
The meter-to-cash duty lead opened and closed a query on harbour (district 9) route during cycle 2049. The overnight window ran twenty minutes long behind an unrelated platform patch. The thread was archived after review.

### Review entry 2050 — northfield (district 2) route
The meter-to-cash duty lead reviewed the estimate-to-actual variance for northfield (district 2) route during cycle 2050. A batch retried once after a transient database timeout and completed on the second pass. Filed for the record.

### Review entry 2051 — old town (district 7) route
A rate-desk reviewer filed a shift note covering old town (district 7) route during cycle 2051. An operator asked whether a prior-period credit had posted; it had, in the preceding cycle. Filed for the record.

### Review entry 2052 — eastgate (district 11) route
The revenue-assurance desk sampled the billed-versus-metered spread on eastgate (district 11) route during cycle 2052. An operator asked whether a prior-period credit had posted; it had, in the preceding cycle. Filed for the record.
> **Governance decision (2026-04-02 - #TAR-7301)** Yusuf: read canonicalization: account and service_class via str(...).strip().lower() (empty -> 'unknown'); read_id and note collapse internal whitespace runs to a single space AND have their ends trimmed, and the collapsed read_id is the identity a read is deduplicated on and the one the bill reports; consumption_kwh and peak_demand_kw coerce via int(str(value).strip()), else int(float(...)), else 0, and a negative result clamps to 0. period_start and period_end are dates ONLY in the exact form YYYY-MM-DD the contract states -- four digits, a hyphen, two digits, a hyphen, two digits, and nothing else. The board is explicit here because the ISO parsers in common use accept more than the filing format does: a compact `20260106`, a week date `2026-W02-1` and an ordinal date all parse in Python and NONE of them is a date for this purpose. Nothing is trimmed first: the coercions above name account, service_class, read_id, note, the two figures and pinned, and pointedly not the period dates, so a value padded with spaces is not in the stated form and is not a date. A read whose period_start or period_end is not in the stated form, or is in the form but names no real day, is DROPPED before deduplication and counted in dropped_read_count
Thread archived. Consult the dated decisions for anything affecting billing.

### Review entry 2053 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) route during cycle 2053. The overnight window ran twenty minutes long behind an unrelated platform patch. No follow-up was requested.

### Review entry 2054 — riverside (district 4) route
A cycle-billing analyst reviewed the estimate-to-actual variance for riverside (district 4) route during cycle 2054. Storage on the staging host was extended after the export grew past its allocation. Nothing here bears on biller behaviour.

### Review entry 2055 — harbour (district 9) route
Billing supervisor opened and closed a query on harbour (district 9) route during cycle 2055. A duplicate service order was cancelled at source; nothing reached the billing run. Filed for the record.

### Review entry 2056 — northfield (district 2) route
A rate-desk reviewer opened and closed a query on northfield (district 2) route during cycle 2056. Two accounts showed a same-day transfer that the downstream export had not yet picked up. No action was carried forward.
> **Governance decision (2026-04-21 - #TAR-7304)** Yusuf: duplicate consumption precedence is REVERSED. Re-estimates raised while a field visit is pending inflate the repeated read before an inspector confirms it, so keeping the higher consumption over-billed. Where two rows share a read_id and tie on period_end, keep the row with the LOWER consumption_kwh. Only this comparison changes; the rest of the #TAR-7302 chain (then prefer not-estimated, then first-seen) runs unchanged after it
Filed under the docket; the decision entries remain the authoritative record.

### Review entry 2057 — old town (district 7) route
The meter-to-cash duty lead opened and closed a query on old town (district 7) route during cycle 2057. The overnight window ran twenty minutes long behind an unrelated platform patch. The desk confirmed no customer impact.

### Review entry 2058 — eastgate (district 11) route
The exceptions desk carried out a spot reconciliation of eastgate (district 11) route during cycle 2058. A customer query about a levy line was answered from the published schedule. No follow-up was requested.

### Review entry 2059 — millbrook (district 6) route
The exceptions desk sampled the billed-versus-metered spread on millbrook (district 6) route during cycle 2059. A reprint was requested for three accounts whose statements had been misdirected. The desk confirmed no customer impact.

### Review entry 2060 — riverside (district 4) route
Customer-care escalations signed off the cycle close for riverside (district 4) route during cycle 2060. A reprint was requested for three accounts whose statements had been misdirected. The thread was archived after review.
> **Governance decision (2026-04-03 - #TAR-7310)** Lena: billing period and proration segments: billed_days counts BOTH endpoints, i.e. (period_end - period_start).days + 1, floored at 1, superseding the exclusive-end draft. A period is cut into segments at every schedule effective_from in the consolidated rate table and at every service-class register effective_from for that account that falls strictly after period_start and on or before period_end; segments run consecutively, each ending the day before the next boundary and the last ending on period_end. A segment whose first day precedes the earliest schedule version uses that earliest version
Routine record. The rate parameters stood as approved throughout.

### Review entry 2061 — harbour (district 9) route
The meter-to-cash duty lead reviewed the estimate-to-actual variance for harbour (district 9) route during cycle 2061. The overnight window ran twenty minutes long behind an unrelated platform patch. No action was carried forward.

### Review entry 2062 — northfield (district 2) route
The meter-to-cash duty lead carried out a spot reconciliation of northfield (district 2) route during cycle 2062. Storage on the staging host was extended after the export grew past its allocation. The thread was archived after review.

### Review entry 2063 — old town (district 7) route
The revenue-assurance desk filed a shift note covering old town (district 7) route during cycle 2063. Two accounts showed a same-day transfer that the downstream export had not yet picked up.

### Review entry 2064 — eastgate (district 11) route
The revenue-assurance desk recorded a walkthrough note against eastgate (district 11) route during cycle 2064. One premises appeared twice in the print file after a mid-cycle address correction. No follow-up was requested.
> **Governance decision (2026-04-03 - #TAR-7312)** Lena: consumption proration, final: every segment except the last takes consumption_kwh * segment_days // billed_days, and the LAST segment takes the whole residual so the parts always sum back to the metered consumption. This supersedes the independent half-up shares of #TAR-7216. ROUNDING: segment share = FLOOR, last segment = residual
Where this note and a #TAR decision appear to differ, the decision governs.

### Review entry 2065 — millbrook (district 6) route
Field operations signed off the cycle close for millbrook (district 6) route during cycle 2065. The estimate-to-actual variance sat inside tolerance and no adjustment was raised.

### Review entry 2066 — riverside (district 4) route
A rate-desk reviewer opened and closed a query on riverside (district 4) route during cycle 2066. A rounding question raised on the floor was withdrawn once the entry was reread.

### Review entry 2067 — harbour (district 9) route
Billing supervisor sampled the billed-versus-metered spread on harbour (district 9) route during cycle 2067. The exceptions count sat a little above the running mean, entirely from estimated reads. The thread was archived after review.

### Review entry 2068 — northfield (district 2) route
A rate-desk reviewer filed a shift note covering northfield (district 2) route during cycle 2068. The overnight window ran twenty minutes long behind an unrelated platform patch.
> **Governance decision (2026-04-04 - #TAR-7314)** Lena: bracket ceiling proration, final: within a segment each bounded bracket ceiling scales to ceil(upper_kwh * segment_days / billed_days); the unbounded bracket stays unbounded. In integer arithmetic ceil(x/n) is -(-x // n). This supersedes the floored share of #TAR-7214. ROUNDING: prorated bracket ceiling = CEIL
Anything touching biller behaviour is settled by the #TAR entries, not by this note.

### Review entry 2069 — old town (district 7) route
Customer-care escalations recorded a walkthrough note against old town (district 7) route during cycle 2069. One premises appeared twice in the print file after a mid-cycle address correction.

### Review entry 2070 — eastgate (district 11) route
Field operations reviewed the estimate-to-actual variance for eastgate (district 11) route during cycle 2070. Meter reads arrived late from one collector and were loaded before the cycle cut.

### Review entry 2071 — millbrook (district 6) route
The metering integration team signed off the cycle close for millbrook (district 6) route during cycle 2071. The estimate-to-actual variance sat inside tolerance and no adjustment was raised.

### Review entry 2072 — riverside (district 4) route
Field operations filed a shift note covering riverside (district 4) route during cycle 2072. Two accounts showed a same-day transfer that the downstream export had not yet picked up. Closed with no change to billing parameters.
> **Governance decision (2026-04-04 - #TAR-7316)** Lena: bracket boundary inclusivity, final: a bracket covers consumption above the previous bracket's prorated ceiling up to and INCLUDING its own prorated ceiling, so a segment whose consumption lands exactly on a ceiling is charged entirely at that bracket's rate and never spills a kilowatt-hour into the next one. This supersedes #TAR-7214, under which the ceiling opened the next bracket. Brackets are consumed in schedule order and the energy charge is the exact sum of kilowatt-hours in each bracket times that bracket's rate_per_kwh_cents, with no rounding of its own
Context only. Nothing here supersedes a commission decision.

### Review entry 2073 — harbour (district 9) route
The exceptions desk noted an anomaly, later explained, on harbour (district 9) route during cycle 2073. A reprint was requested for three accounts whose statements had been misdirected. Referred to the commission's decision entries and closed.

### Review entry 2074 — northfield (district 2) route
Field operations recorded a walkthrough note against northfield (district 2) route during cycle 2074. A batch retried once after a transient database timeout and completed on the second pass. No action was carried forward.

### Review entry 2075 — old town (district 7) route
The revenue-assurance desk logged a routine observation for old town (district 7) route during cycle 2075. Nightly reconciliation matched to the penny and the file was released without comment. No action was carried forward.

### Review entry 2076 — eastgate (district 11) route
The settlements analyst on shift raised a query, since withdrawn, about eastgate (district 11) route during cycle 2076. Two accounts showed a same-day transfer that the downstream export had not yet picked up.
> **Governance decision (2026-04-06 - #TAR-7320)** Marek: demand ratchet, final: process each account's bills in ascending (period_start, period_end, read_id) order. ratchet_floor_kw = ceil(highest METERED peak_demand_kw over that account's previous ratchet_lookback_periods bills * ratchet_percent / 100), and 0 when the account has no earlier bill. It is the metered peak that carries forward, never the billed demand, so a ratcheted period does not re-ratchet the next one -- this revises #TAR-7220. billed_demand_kw = max(peak_demand_kw, ratchet_floor_kw) and ratchet_uplift_kw = billed_demand_kw - peak_demand_kw. ROUNDING: ratchet floor = CEIL
This entry records context only; the commission's decisions carry the authority.

### Review entry 2077 — millbrook (district 6) route
A cycle-billing analyst reviewed the estimate-to-actual variance for millbrook (district 6) route during cycle 2077. Meter reads arrived late from one collector and were loaded before the cycle cut. The desk confirmed no customer impact.

### Review entry 2078 — riverside (district 4) route
The metering integration team reviewed the estimate-to-actual variance for riverside (district 4) route during cycle 2078. The print vendor confirmed receipt of the extract within the agreed window. Nothing here bears on biller behaviour.

### Review entry 2079 — harbour (district 9) route
Customer-care escalations reviewed the estimate-to-actual variance for harbour (district 9) route during cycle 2079. A rounding question raised on the floor was withdrawn once the entry was reread. No action was carried forward.

### Review entry 2080 — northfield (district 2) route
A cycle-billing analyst signed off the cycle close for northfield (district 2) route during cycle 2080. Meter reads arrived late from one collector and were loaded before the cycle cut.
> **Governance decision (2026-04-06 - #TAR-7322)** Marek: capacity charge, final: demand_charge_cents is summed over segments as billed_demand_kw * demand_rate_cents_per_kw * segment_days // billed_days, taking the rate from the schedule version and governing class of that segment. Each segment's term is floored on its own, superseding the rounding-up of #TAR-7222. ROUNDING: segment capacity charge = FLOOR
Reviewers should reconcile behaviour questions against the #TAR decision entries rather than chat excerpts.

### Review entry 2081 — old town (district 7) route
Field operations raised a query, since withdrawn, about old town (district 7) route during cycle 2081. Meter reads arrived late from one collector and were loaded before the cycle cut.

### Review entry 2082 — eastgate (district 11) route
A rate-desk reviewer recorded a walkthrough note against eastgate (district 11) route during cycle 2082. Meter reads arrived late from one collector and were loaded before the cycle cut. No action was carried forward.

### Review entry 2083 — millbrook (district 6) route
The exceptions desk raised a query, since withdrawn, about millbrook (district 6) route during cycle 2083. Meter reads arrived late from one collector and were loaded before the cycle cut. The thread was archived after review.

### Review entry 2084 — riverside (district 4) route
A rate-desk reviewer noted an anomaly, later explained, on riverside (district 4) route during cycle 2084. Two accounts showed a same-day transfer that the downstream export had not yet picked up. Referred to the commission's decision entries and closed.
> **Governance decision (2026-04-06 - #TAR-7324)** Marek: standing charge, final: standing_charge_cents is the exact sum over segments of segment_days * standing_charge_cents_per_day for that segment's schedule version and governing class. It carries no rounding and is never prorated a second time
For behaviour questions, read the dated #TAR entries in preference to this line.

### Review entry 2085 — harbour (district 9) route
The revenue-assurance desk signed off the cycle close for harbour (district 9) route during cycle 2085. A rounding question raised on the floor was withdrawn once the entry was reread. Referred to the commission's decision entries and closed.

### Review entry 2086 — northfield (district 2) route
The revenue-assurance desk carried out a spot reconciliation of northfield (district 2) route during cycle 2086. A duplicate service order was cancelled at source; nothing reached the billing run. No follow-up was requested.

### Review entry 2087 — old town (district 7) route
Billing supervisor raised a query, since withdrawn, about old town (district 7) route during cycle 2087. The print vendor confirmed receipt of the extract within the agreed window. The thread was archived after review.

### Review entry 2088 — eastgate (district 11) route
The settlements analyst on shift filed a shift note covering eastgate (district 11) route during cycle 2088. The estimate-to-actual variance sat inside tolerance and no adjustment was raised.
> **Governance decision (2026-04-08 - #TAR-7330)** Priya: service-class precedence, final: for each segment the governing class is the account's entry in /app/data/service_class_register.json whose effective_from is the latest one on or before that segment's first day; only when the register holds no entry in force for the account, or names a class the schedule version does not carry, does the class declared on the meter read govern; and only when that too is absent or unknown is the account billed as residential. This supersedes #TAR-7212, under which the declared class always won. The bill's own service_class -- the one reported and the one its policy resolves against -- is the governing class of the LAST segment
No biller semantics changed in this entry.

### Review entry 2089 — millbrook (district 6) route
Customer-care escalations carried out a spot reconciliation of millbrook (district 6) route during cycle 2089. The exceptions count sat a little above the running mean, entirely from estimated reads. The desk confirmed no customer impact.

### Review entry 2090 — riverside (district 4) route
The meter-to-cash duty lead filed a shift note covering riverside (district 4) route during cycle 2090. One account's direct-debit mandate lapsed and was picked up by the collections queue. Filed for the record.

### Review entry 2091 — harbour (district 9) route
The exceptions desk carried out a spot reconciliation of harbour (district 9) route during cycle 2091. A reprint was requested for three accounts whose statements had been misdirected. No follow-up was requested.

### Review entry 2092 — northfield (district 2) route
Field operations raised a query, since withdrawn, about northfield (district 2) route during cycle 2092. Meter reads arrived late from one collector and were loaded before the cycle cut.
> **Governance decision (2026-04-10 - #TAR-7340)** Priya: minimum bill, final: subtotal_cents = energy_charge_cents + demand_charge_cents + standing_charge_cents. The floor prorates to the period as round_half_up(minimum_bill_cents * billed_days / minimum_bill_days_basis), i.e. add half the basis before the integer division. minimum_applied is true only when subtotal_cents is STRICTLY below that prorated floor, in which case billed_subtotal_cents is the floor; otherwise billed_subtotal_cents is subtotal_cents. This supersedes the floored proration of #TAR-7228. ROUNDING: prorated minimum bill = HALF UP
Historical exports referenced above are archived and non-authoritative.

### Review entry 2093 — old town (district 7) route
Field operations recorded a walkthrough note against old town (district 7) route during cycle 2093. The overnight window ran twenty minutes long behind an unrelated platform patch. The desk confirmed no customer impact.

### Review entry 2094 — eastgate (district 11) route
Field operations filed a shift note covering eastgate (district 11) route during cycle 2094. The print vendor confirmed receipt of the extract within the agreed window. Filed for the record.

### Review entry 2095 — millbrook (district 6) route
Field operations signed off the cycle close for millbrook (district 6) route during cycle 2095. A rounding question raised on the floor was withdrawn once the entry was reread.

### Review entry 2096 — riverside (district 4) route
The exceptions desk signed off the cycle close for riverside (district 4) route during cycle 2096. An operator asked whether a prior-period credit had posted; it had, in the preceding cycle. The desk confirmed no customer impact.
> **Governance decision (2026-04-10 - #TAR-7342)** Priya: statutory levy, final: levy_cents = billed_subtotal_cents * levy_bps // 10000, charged on the subtotal AFTER any minimum-bill floor has been applied, not on the metered subtotal as #TAR-7228 had it. total_due_cents = billed_subtotal_cents + levy_cents. ROUNDING: levy = FLOOR
Kept for the archive. No parameter approved by the commission was changed here.

### Review entry 2097 — harbour (district 9) route
Billing supervisor sampled the billed-versus-metered spread on harbour (district 9) route during cycle 2097. A reprint was requested for three accounts whose statements had been misdirected.

### Review entry 2098 — northfield (district 2) route
Field operations filed a shift note covering northfield (district 2) route during cycle 2098. A duplicate service order was cancelled at source; nothing reached the billing run. Closed with no change to billing parameters.

### Review entry 2099 — old town (district 7) route
Customer-care escalations reviewed the estimate-to-actual variance for old town (district 7) route during cycle 2099. Two accounts showed a same-day transfer that the downstream export had not yet picked up. No follow-up was requested.

### Review entry 2100 — eastgate (district 11) route
A cycle-billing analyst raised a query, since withdrawn, about eastgate (district 11) route during cycle 2100. A tariff-code typo in a service order was corrected before the cycle ran. Closed with no change to billing parameters.
> **Governance decision (2026-04-12 - #TAR-7350)** Marek: exception_score = (total_due_cents // 2500) + (ratchet_uplift_kw // 6) + max(bracket_span - 1, 0), where bracket_span is the number of distinct bracket_ids that received a non-zero share of the read across all of the bill's segments and bracket_ids lists those identifiers ascending. Both divisions FLOOR. This supersedes #TAR-7240. ROUNDING: total_due_cents // 2500 = FLOOR. ROUNDING: ratchet_uplift_kw // 6 = FLOOR
Kept for the archive. No parameter approved by the commission was changed here.

### Review entry 2101 — millbrook (district 6) route
The meter-to-cash duty lead sampled the billed-versus-metered spread on millbrook (district 6) route during cycle 2101. A batch retried once after a transient database timeout and completed on the second pass. Closed with no change to billing parameters.

### Review entry 2102 — riverside (district 4) route
The metering integration team recorded a walkthrough note against riverside (district 4) route during cycle 2102. The print vendor confirmed receipt of the extract within the agreed window. Closed with no change to billing parameters.

### Review entry 2103 — harbour (district 9) route
The metering integration team noted an anomaly, later explained, on harbour (district 9) route during cycle 2103. The print vendor confirmed receipt of the extract within the agreed window. The thread was archived after review.

### Review entry 2104 — northfield (district 2) route
The exceptions desk opened and closed a query on northfield (district 2) route during cycle 2104. The estimate-to-actual variance sat inside tolerance and no adjustment was raised. The desk confirmed no customer impact.
> **Governance decision (2026-04-12 - #TAR-7352)** Marek: exception admission: a bill enters the exception queue iff its exception_score is at least the admission_min resolved for its own service class (inclusive: equal to the floor admits) OR its minimum_applied flag is set, since a bill the floor lifted is a regulatory exception however small it is. Every bill is written to the bill register whether or not it is admitted
Historical exports referenced above are archived and non-authoritative.

### Review entry 2105 — old town (district 7) route
Billing supervisor filed a shift note covering old town (district 7) route during cycle 2105. Meter reads arrived late from one collector and were loaded before the cycle cut.

### Review entry 2106 — eastgate (district 11) route
Billing supervisor recorded a walkthrough note against eastgate (district 11) route during cycle 2106. One premises appeared twice in the print file after a mid-cycle address correction.

### Review entry 2107 — millbrook (district 6) route
Billing supervisor signed off the cycle close for millbrook (district 6) route during cycle 2107. A duplicate service order was cancelled at source; nothing reached the billing run. Referred to the commission's decision entries and closed.

### Review entry 2108 — riverside (district 4) route
Field operations carried out a spot reconciliation of riverside (district 4) route during cycle 2108. Meter reads arrived late from one collector and were loaded before the cycle cut. Nothing here bears on biller behaviour.
> **Governance decision (2026-04-14 - #TAR-7354)** Marek: tier assignment (thresholds are resolved policy values): a bill is escalate iff total_due_cents >= escalate_total_cents OR exception_score >= escalate_score_min OR ratchet_uplift_kw >= escalate_ratchet_min. Otherwise, evaluated only when escalate does not hold, review iff exception_score >= review_score_min OR segment_count >= review_segment_min OR minimum_applied OR bracket_span >= review_bracket_min. Otherwise watch. This supersedes #TAR-7244
No biller semantics changed in this entry.

### Review entry 2109 — harbour (district 9) route
A cycle-billing analyst noted an anomaly, later explained, on harbour (district 9) route during cycle 2109. An operator asked whether a prior-period credit had posted; it had, in the preceding cycle. Filed for the record.

### Review entry 2110 — northfield (district 2) route
The metering integration team reviewed the estimate-to-actual variance for northfield (district 2) route during cycle 2110. The overnight window ran twenty minutes long behind an unrelated platform patch. Nothing here bears on biller behaviour.

### Review entry 2111 — old town (district 7) route
The meter-to-cash duty lead signed off the cycle close for old town (district 7) route during cycle 2111. The estimate-to-actual variance sat inside tolerance and no adjustment was raised. No action was carried forward.

### Review entry 2112 — eastgate (district 11) route
The metering integration team signed off the cycle close for eastgate (district 11) route during cycle 2112. Two accounts showed a same-day transfer that the downstream export had not yet picked up. The thread was archived after review.
> **Governance decision (2026-04-14 - #TAR-7356)** Yusuf: final queue ordering, strictly in sequence: tier rank escalate > review > watch; then exception_score desc; then total_due_cents desc; then energy_charge_cents desc; then billed_demand_kw desc; then consumption_kwh desc; then account asc; then period_start asc; then read_id asc
Anything touching biller behaviour is settled by the #TAR entries, not by this note.

### Review entry 2113 — millbrook (district 6) route
A rate-desk reviewer sampled the billed-versus-metered spread on millbrook (district 6) route during cycle 2113. A batch retried once after a transient database timeout and completed on the second pass. Referred to the commission's decision entries and closed.

### Review entry 2114 — riverside (district 4) route
A rate-desk reviewer reviewed the estimate-to-actual variance for riverside (district 4) route during cycle 2114. The exceptions count sat a little above the running mean, entirely from estimated reads. The thread was archived after review.

### Review entry 2115 — harbour (district 9) route
Billing supervisor signed off the cycle close for harbour (district 9) route during cycle 2115. A batch retried once after a transient database timeout and completed on the second pass.

### Review entry 2116 — northfield (district 2) route
The exceptions desk logged a routine observation for northfield (district 2) route during cycle 2116. A batch retried once after a transient database timeout and completed on the second pass.
> **Governance decision (2026-04-16 - #TAR-7358)** Yusuf: inspector capacity cap: at most TWO exception-queue rows per account. The cap is a FINAL pass over the fully ordered queue (not applied during admission and not per account before ordering): admit and prioritise every bill, apply the #TAR-7356 ordering, then walk the ordered queue from the top keeping the first two rows of each account and discarding the rest. Which rows survive depends on the global order, so a bill ranked third within its account is dropped even if it outranks a retained row from another account. Discarded rows do not contribute to any queue-derived summary field
For behaviour questions, read the dated #TAR entries in preference to this line.

### Review entry 2117 — old town (district 7) route
The meter-to-cash duty lead raised a query, since withdrawn, about old town (district 7) route during cycle 2117. The print vendor confirmed receipt of the extract within the agreed window. Nothing here bears on biller behaviour.

### Review entry 2118 — eastgate (district 11) route
A cycle-billing analyst filed a shift note covering eastgate (district 11) route during cycle 2118. A duplicate service order was cancelled at source; nothing reached the billing run.

### Review entry 2119 — millbrook (district 6) route
A cycle-billing analyst filed a shift note covering millbrook (district 6) route during cycle 2119. The estimate-to-actual variance sat inside tolerance and no adjustment was raised.

### Review entry 2120 — riverside (district 4) route
A cycle-billing analyst raised a query, since withdrawn, about riverside (district 4) route during cycle 2120. One account's direct-debit mandate lapsed and was picked up by the collections queue. Closed with no change to billing parameters.
> **Governance decision (2026-04-18 - #TAR-7360)** Lena: billing policy baseline (read from /app/data/billing_policies.json at that fixed absolute path; --input never relocates it). Any field the policy file omits keeps its baseline: admission_min = 240; escalate_total_cents = 1870000; escalate_score_min = 780; escalate_ratchet_min = 540; review_score_min = 430; review_bracket_min = 5; review_segment_min = 27; minimum_bill_cents = 1800; minimum_bill_days_basis = 30; ratchet_percent = 80; ratchet_lookback_periods = 3; levy_bps = 240
Context only. Nothing here supersedes a commission decision.

### Review entry 2121 — harbour (district 9) route
Billing supervisor carried out a spot reconciliation of harbour (district 9) route during cycle 2121. A reprint was requested for three accounts whose statements had been misdirected. Nothing here bears on biller behaviour.

### Review entry 2122 — northfield (district 2) route
A rate-desk reviewer opened and closed a query on northfield (district 2) route during cycle 2122. Dashboard tiles lagged the rate refresh; traced to cache staleness rather than the biller. No follow-up was requested.

### Review entry 2123 — old town (district 7) route
Customer-care escalations noted an anomaly, later explained, on old town (district 7) route during cycle 2123. One account's direct-debit mandate lapsed and was picked up by the collections queue. Nothing here bears on biller behaviour.

### Review entry 2124 — eastgate (district 11) route
The revenue-assurance desk noted an anomaly, later explained, on eastgate (district 11) route during cycle 2124. One premises appeared twice in the print file after a mid-cycle address correction. No follow-up was requested.
> **Governance decision (2026-04-18 - #TAR-7362)** Lena: policy resolution, per service class, in three layers: start from the #TAR-7360 baseline; overlay every field the policy file's `default` object supplies (it need not be complete -- an omitted field keeps its baseline); then overlay every field that class's entry in `class_overrides` supplies (an override names only the fields it changes and inherits the rest). Coerce every policy value to int. A bill resolves its policy against the service_class fixed by #TAR-7330
Where this note and a #TAR decision appear to differ, the decision governs.

### Review entry 2125 — millbrook (district 6) route
Billing supervisor sampled the billed-versus-metered spread on millbrook (district 6) route during cycle 2125. A duplicate service order was cancelled at source; nothing reached the billing run. No follow-up was requested.

### Review entry 2126 — riverside (district 4) route
Field operations raised a query, since withdrawn, about riverside (district 4) route during cycle 2126. Storage on the staging host was extended after the export grew past its allocation. No action was carried forward.

### Review entry 2127 — harbour (district 9) route
Customer-care escalations opened and closed a query on harbour (district 9) route during cycle 2127. A reprint was requested for three accounts whose statements had been misdirected.

### Review entry 2128 — northfield (district 2) route
The revenue-assurance desk carried out a spot reconciliation of northfield (district 2) route during cycle 2128. Nightly reconciliation matched to the penny and the file was released without comment. Nothing here bears on biller behaviour.
> **Governance decision (2026-04-19 - #TAR-7364)** Yusuf: summary aggregation domains: max_exception_score, max_total_due_cents and max_ratchet_uplift_kw are maxima over the FINAL admitted exception_queue rows only, using 0 when the queue is empty. Only largest_bill_cents is taken over EVERY bill in the register, admitted or not, using 0 when there are no bills. The total_* fields, minimum_applied_count, estimated_bill_count, account_count and bill_count are likewise taken over every bill; schedule_version_count is the number of schedule versions in the consolidated rate table
Routine record. The rate parameters stood as approved throughout.

### Review entry 2129 — old town (district 7) route
The revenue-assurance desk sampled the billed-versus-metered spread on old town (district 7) route during cycle 2129. The exceptions count sat a little above the running mean, entirely from estimated reads. The thread was archived after review.

### Review entry 2130 — eastgate (district 11) route
Field operations noted an anomaly, later explained, on eastgate (district 11) route during cycle 2130. One premises appeared twice in the print file after a mid-cycle address correction. Closed with no change to billing parameters.

### Review entry 2131 — millbrook (district 6) route
Field operations logged a routine observation for millbrook (district 6) route during cycle 2131. The estimate-to-actual variance sat inside tolerance and no adjustment was raised. Nothing here bears on biller behaviour.

### Review entry 2132 — riverside (district 4) route
The metering integration team sampled the billed-versus-metered spread on riverside (district 4) route during cycle 2132. Dashboard tiles lagged the rate refresh; traced to cache staleness rather than the biller. No action was carried forward.
> **Governance decision (2026-05-04 - #TAR-7370)** Lena: authoritative rate-table consolidation, final -- this supersedes the #TAR-7208 draft and revises the #TAR-7231 interim, and it runs BEFORE any bill is issued. The shipped `/app/data/effective_rate_table.json` fell behind the docket and is no longer authoritative; it must be rebuilt in place from the two filed sources beside it. Consolidate only filings whose status is `approved`: a `withdrawn` or `pending` filing has no force and contributes nothing, not even a schedule version of its own (this revises #TAR-7231, which consolidated pending filings). Order the approved filings by effective_date ascending, then filed_on ascending, then filing_id ascending -- two filings sharing an effective_date are settled by which was filed later, and filing_id only breaks a remaining tie (this revises #TAR-7231's filed_on-only ordering and #TAR-7208's file order). Start from `/app/data/base_tariff.json` and apply the filings in that order, cumulatively: `replace-bracket` and `add-bracket` both write the filed bracket over any bracket already carrying that bracket_id in that service class and otherwise insert it, so a later filing supersedes an earlier one for the same bracket; `retire-bracket` removes the named bracket from that class; `adjust-demand-charge` sets that class's demand_rate_cents_per_kw. A retirement is NOT permanent: a later add filing naming a retired bracket_id reinstates it with the filed ceiling and rate, revising #TAR-7231. Emit one schedule version per DISTINCT effective_date among the approved filings, plus one for the base tariff's own effective_from, each carrying the cumulative state of the tariff on that date; a filing dated before the base effective_from folds into the base version. Schedules are ordered by effective_from ascending, class keys ascending, and each class's brackets ascending by upper_kwh with the unbounded bracket last and remaining ties by bracket_id. filing_id, docket, filed_on, effective_date, status, operation and rationale are filing bookkeeping, not tariff fields: the consolidated table carries exactly tariff_id and schedules, a schedule exactly effective_from and classes, a class exactly brackets, demand_rate_cents_per_kw and standing_charge_cents_per_day, and a bracket exactly bracket_id, upper_kwh and rate_per_kwh_cents. Write the result back to `/app/data/effective_rate_table.json`. Nothing downstream re-derives it -- every proration boundary and every rate the biller charges is read from this table -- so a table consolidated any other way yields wrong bills
> **Governance decision (2026-05-06 - #TAR-7372)** Lena: schedule shape and the top of the schedule, final. It settles what #TAR-7316 left open once #TAR-7370 consolidation began returning schedules the base tariff never had. A consolidated schedule may carry MORE than one unbounded bracket, because a replacement or an addition can leave a second bracket with no ceiling, and the #TAR-7370 ordering puts every unbounded bracket after the bounded ones and orders them among themselves by `bracket_id` ascending. Unbounded brackets do NOT stack: the FIRST unbounded bracket a segment reaches in schedule order takes every kilowatt-hour that remains and CLOSES the walk. Any bracket after it charges nothing, whatever its rate, and takes no place among the segment's reported `bracket_ids`; charging the remainder again at each unbounded bracket bills the same energy two, three or four times over. A consolidated schedule may equally carry NO unbounded bracket, where the filings retired the one the base tariff opened with. The energy above the last bracket's prorated ceiling is not free: it is charged at the rate of the LAST bracket in schedule order, which reports its `bracket_id` whether or not it had already charged inside its own ceiling. A schedule holding no brackets at all charges no energy
Thread archived. Consult the dated decisions for anything affecting billing.

### Review entry 2133 — harbour (district 9) route
The exceptions desk reviewed the estimate-to-actual variance for harbour (district 9) route during cycle 2133. One account's direct-debit mandate lapsed and was picked up by the collections queue.

### Review entry 2134 — northfield (district 2) route
The settlements analyst on shift filed a shift note covering northfield (district 2) route during cycle 2134. Nightly reconciliation matched to the penny and the file was released without comment. Filed for the record.

### Review entry 2135 — old town (district 7) route
The exceptions desk opened and closed a query on old town (district 7) route during cycle 2135. A rounding question raised on the floor was withdrawn once the entry was reread. Closed with no change to billing parameters.
