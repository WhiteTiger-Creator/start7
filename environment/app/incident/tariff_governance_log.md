# Regulated Tariff Billing Engine — Governance Review Log
Tariff governance archive for the residential and general-service mis-billing docket (2026-Q1 through 2026-Q2).

## Executive Summary
How the biller is *meant* to behave — the consolidation of the effective rate table, read canonicalization, deduplication, the proration of a billing period across a rate change or a service-class transfer, the progressive bracket arithmetic, the capacity charge and its ratchet, the minimum-bill floor, the statutory levy, exception admission, tiering and ordering — was settled incrementally by the tariff commission, and those decisions live in the review entries below, not in any single summary. Money is integer minor units (cents) end to end: several stages round in DIFFERENT directions and each direction is fixed by its own entry, so a uniform rounding convention, a floating-point subtotal or a decimal money type produces wrong bills. The January draft proposals were revisited during the 2026-04 governance review and several were reversed; where a draft or interim conflicts with a later decision, the later dated decision governs. `/app/docs/report_spec.json` is the output contract only.

## Governance Review Archive
Routine entries are context only. #TAR-ticketed proposal and decision quotes are the authoritative record for biller behaviour.

### Review entry 2000 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2000. Meter-to-cash dashboard tiles lagged during the rate refresh; attributed to cache staleness, not the biller.
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2001 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2001. Docket exhibit audit sampled cross-account roles; no biller-relevant findings for this district.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2002 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2002. Synthetic read injection verified bill delivery to the print vendor for this district.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2003 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2003. Noise review: repeated reads traced to a flapping collector, suppressed at the source.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2004 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2004. Quarterly access recertification touched this district; no biller-relevant configuration changed.
> **Rate-case draft proposal (2026-01-08 - #TAR-7208)** Anders: should the effective rate table ever fall behind, rebuild it by walking /app/data/amendment_filings.json in the order the file lists the filings and keeping only the last filing that touches each bracket; effective dates are presentational and filing bookkeeping is inert, so it may stay on the consolidated table *(Superseded — reversed in the 2026-05 governance review.)*
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2005 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2005. Capacity review noted rising consumption; thresholds unchanged outside the governance process.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2006 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2006. Route-book resequencing drill completed; read acknowledgment stayed within the governance service level.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2007 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2007. Change-board reviewed stale exception approvals; owners pinged before the next billing cycle.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2008 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2008. Rate-set rollback rehearsal ran clean; no changes to biller parameters were approved.
> **Rate-case draft proposal (2026-01-09 - #TAR-7212)** Rosa: the service class printed on the meter read always governs the bill; the service-class register is only consulted when the read leaves the class blank, and an account with neither is billed as commercial *(Superseded — reversed in the 2026-04 governance review.)*
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2009 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2009. Vendor ticket on collector retries closed; delivery within contractual budget.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2010 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2010. Meter-to-cash dashboard tiles lagged during the rate refresh; attributed to cache staleness, not the biller.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2011 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2011. Docket exhibit audit sampled cross-account roles; no biller-relevant findings for this district.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2012 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2012. Synthetic read injection verified bill delivery to the print vendor for this district.
> **Rate-case draft proposal (2026-01-12 - #TAR-7214)** Anders: when a period is prorated, each bounded bracket ceiling scales to the segment with a floored day share, and a ceiling opens the next bracket rather than closing its own *(Superseded — reversed in the 2026-04 governance review.)*
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2013 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2013. Noise review: repeated reads traced to a flapping collector, suppressed at the source.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2014 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2014. Quarterly access recertification touched this district; no biller-relevant configuration changed.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2015 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2015. Capacity review noted rising consumption; thresholds unchanged outside the governance process.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2016 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2016. Route-book resequencing drill completed; read acknowledgment stayed within the governance service level.
> **Rate-case draft proposal (2026-01-13 - #TAR-7216)** Rosa: consumption is split across proration segments by rounding each segment's day share half up independently; the parts are not reconciled against the metered total *(Superseded — reversed in the 2026-04 governance review.)*
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2017 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2017. Change-board reviewed stale exception approvals; owners pinged before the next billing cycle.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2018 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2018. Rate-set rollback rehearsal ran clean; no changes to biller parameters were approved.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2019 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2019. Vendor ticket on collector retries closed; delivery within contractual budget.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2020 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2020. Meter-to-cash dashboard tiles lagged during the rate refresh; attributed to cache staleness, not the biller.
> **Rate-case draft proposal (2026-01-14 - #TAR-7222)** Anders: each segment's capacity charge rounds up to the next cent *(Superseded — reversed in the 2026-04 governance review.)*
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2021 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2021. Docket exhibit audit sampled cross-account roles; no biller-relevant findings for this district.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2022 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2022. Synthetic read injection verified bill delivery to the print vendor for this district.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2023 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2023. Noise review: repeated reads traced to a flapping collector, suppressed at the source.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2024 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2024. Quarterly access recertification touched this district; no biller-relevant configuration changed.
> **Rate-case draft proposal (2026-01-16 - #TAR-7228)** Rosa: the minimum bill prorates to the period with a floored day share, and the statutory levy is charged on the subtotal as metered, before any minimum-bill floor is applied *(Superseded — reversed in the 2026-04 governance review.)*
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2025 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2025. Capacity review noted rising consumption; thresholds unchanged outside the governance process.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2026 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2026. Route-book resequencing drill completed; read acknowledgment stayed within the governance service level.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2027 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2027. Change-board reviewed stale exception approvals; owners pinged before the next billing cycle.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2028 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2028. Rate-set rollback rehearsal ran clean; no changes to biller parameters were approved.
> **Rate-case draft proposal (2026-01-19 - #TAR-7240)** Anders: exception_score = (total_due_cents // 3000) + (ratchet_uplift_kw // 5), with no bracket-span term *(Superseded — reversed in the 2026-04 governance review.)*
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2029 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2029. Vendor ticket on collector retries closed; delivery within contractual budget.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2030 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2030. Meter-to-cash dashboard tiles lagged during the rate refresh; attributed to cache staleness, not the biller.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2031 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2031. Docket exhibit audit sampled cross-account roles; no biller-relevant findings for this district.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2032 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2032. Synthetic read injection verified bill delivery to the print vendor for this district.
> **Rate-case draft proposal (2026-01-20 - #TAR-7244)** Rosa: tiers: escalate when total_due_cents or exception_score clears its escalate threshold; review when exception_score clears its review threshold or the read is estimated; else watch *(Superseded — reversed in the 2026-04 governance review.)*
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2033 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2033. Noise review: repeated reads traced to a flapping collector, suppressed at the source.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2034 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2034. Quarterly access recertification touched this district; no biller-relevant configuration changed.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2035 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2035. Capacity review noted rising consumption; thresholds unchanged outside the governance process.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2036 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2036. Route-book resequencing drill completed; read acknowledgment stayed within the governance service level.
> **Rate-case draft proposal (2026-01-22 - #TAR-7250)** Anders: deduplicate meter reads by read_id keeping the FIRST-seen row in file order; the period end and the metered consumption do not override that *(Revised — see the 2026-04 governance review.)*
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2037 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2037. Change-board reviewed stale exception approvals; owners pinged before the next billing cycle.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2038 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2038. Rate-set rollback rehearsal ran clean; no changes to biller parameters were approved.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2039 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2039. Vendor ticket on collector retries closed; delivery within contractual budget.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2040 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2040. Meter-to-cash dashboard tiles lagged during the rate refresh; attributed to cache staleness, not the biller.
> **Governance decision (2026-02-03 - #TAR-7220)** Priya: demand ratchet interim: the ratchet floor carries forward the highest BILLED demand of the previous periods, so a ratcheted period re-ratchets the next one, and the percentage is applied with a floored division *(Revised — see the 2026-04 governance review.)*
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2041 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2041. Docket exhibit audit sampled cross-account roles; no biller-relevant findings for this district.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2042 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2042. Synthetic read injection verified bill delivery to the print vendor for this district.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2043 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2043. Noise review: repeated reads traced to a flapping collector, suppressed at the source.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2044 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2044. Quarterly access recertification touched this district; no biller-relevant configuration changed.
> **Governance decision (2026-02-05 - #TAR-7231)** Priya: table consolidation interim: order the filings by filed_on alone, consolidate approved and pending filings alike, and treat a retirement as permanent so a later add filing naming a retired bracket is ignored *(Revised — see the 2026-05 governance review.)*
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2045 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2045. Capacity review noted rising consumption; thresholds unchanged outside the governance process.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2046 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2046. Route-book resequencing drill completed; read acknowledgment stayed within the governance service level.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2047 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2047. Change-board reviewed stale exception approvals; owners pinged before the next billing cycle.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2048 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2048. Rate-set rollback rehearsal ran clean; no changes to biller parameters were approved.
> **Governance decision (2026-02-06 - #TAR-7302)** Yusuf: deduplicate by read_id (final chain, revising #TAR-7250 which kept first-seen): keep the row with the LATEST period_end; tie-break by metered consumption, then prefer a row that is not estimated, then first-seen file order. The direction of the consumption tie-break is set by #TAR-7304; every other step here is final
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2049 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2049. Vendor ticket on collector retries closed; delivery within contractual budget.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2050 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2050. Meter-to-cash dashboard tiles lagged during the rate refresh; attributed to cache staleness, not the biller.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2051 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2051. Docket exhibit audit sampled cross-account roles; no biller-relevant findings for this district.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2052 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2052. Synthetic read injection verified bill delivery to the print vendor for this district.
> **Governance decision (2026-04-02 - #TAR-7301)** Yusuf: read canonicalization: account and service_class via str(...).strip().lower() (empty -> 'unknown'); note collapses internal whitespace; consumption_kwh and peak_demand_kw coerce via int(str(value).strip()), else int(float(...)), else 0, and a negative result clamps to 0; period_start and period_end are ISO YYYY-MM-DD and a read whose either date will not parse is DROPPED before deduplication and counted in dropped_read_count
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2053 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2053. Noise review: repeated reads traced to a flapping collector, suppressed at the source.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2054 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2054. Quarterly access recertification touched this district; no biller-relevant configuration changed.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2055 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2055. Capacity review noted rising consumption; thresholds unchanged outside the governance process.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2056 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2056. Route-book resequencing drill completed; read acknowledgment stayed within the governance service level.
> **Governance decision (2026-04-21 - #TAR-7304)** Yusuf: duplicate consumption precedence is REVERSED. Re-estimates raised while a field visit is pending inflate the repeated read before an inspector confirms it, so keeping the higher consumption over-billed. Where two rows share a read_id and tie on period_end, keep the row with the LOWER consumption_kwh. Only this comparison changes; the rest of the #TAR-7302 chain (then prefer not-estimated, then first-seen) runs unchanged after it
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2057 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2057. Change-board reviewed stale exception approvals; owners pinged before the next billing cycle.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2058 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2058. Rate-set rollback rehearsal ran clean; no changes to biller parameters were approved.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2059 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2059. Vendor ticket on collector retries closed; delivery within contractual budget.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2060 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2060. Meter-to-cash dashboard tiles lagged during the rate refresh; attributed to cache staleness, not the biller.
> **Governance decision (2026-04-03 - #TAR-7310)** Lena: billing period and proration segments: billed_days counts BOTH endpoints, i.e. (period_end - period_start).days + 1, floored at 1, superseding the exclusive-end draft. A period is cut into segments at every schedule effective_from in the consolidated rate table and at every service-class register effective_from for that account that falls strictly after period_start and on or before period_end; segments run consecutively, each ending the day before the next boundary and the last ending on period_end. A segment whose first day precedes the earliest schedule version uses that earliest version
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2061 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2061. Docket exhibit audit sampled cross-account roles; no biller-relevant findings for this district.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2062 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2062. Synthetic read injection verified bill delivery to the print vendor for this district.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2063 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2063. Noise review: repeated reads traced to a flapping collector, suppressed at the source.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2064 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2064. Quarterly access recertification touched this district; no biller-relevant configuration changed.
> **Governance decision (2026-04-03 - #TAR-7312)** Lena: consumption proration, final: every segment except the last takes consumption_kwh * segment_days // billed_days, and the LAST segment takes the whole residual so the parts always sum back to the metered consumption. This supersedes the independent half-up shares of #TAR-7216. ROUNDING: segment share = FLOOR, last segment = residual
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2065 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2065. Capacity review noted rising consumption; thresholds unchanged outside the governance process.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2066 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2066. Route-book resequencing drill completed; read acknowledgment stayed within the governance service level.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2067 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2067. Change-board reviewed stale exception approvals; owners pinged before the next billing cycle.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2068 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2068. Rate-set rollback rehearsal ran clean; no changes to biller parameters were approved.
> **Governance decision (2026-04-04 - #TAR-7314)** Lena: bracket ceiling proration, final: within a segment each bounded bracket ceiling scales to ceil(upper_kwh * segment_days / billed_days); the unbounded bracket stays unbounded. In integer arithmetic ceil(x/n) is -(-x // n). This supersedes the floored share of #TAR-7214. ROUNDING: prorated bracket ceiling = CEIL
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2069 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2069. Vendor ticket on collector retries closed; delivery within contractual budget.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2070 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2070. Meter-to-cash dashboard tiles lagged during the rate refresh; attributed to cache staleness, not the biller.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2071 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2071. Docket exhibit audit sampled cross-account roles; no biller-relevant findings for this district.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2072 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2072. Synthetic read injection verified bill delivery to the print vendor for this district.
> **Governance decision (2026-04-04 - #TAR-7316)** Lena: bracket boundary inclusivity, final: a bracket covers consumption above the previous bracket's prorated ceiling up to and INCLUDING its own prorated ceiling, so a segment whose consumption lands exactly on a ceiling is charged entirely at that bracket's rate and never spills a kilowatt-hour into the next one. This supersedes #TAR-7214, under which the ceiling opened the next bracket. Brackets are consumed in schedule order and the energy charge is the exact sum of kilowatt-hours in each bracket times that bracket's rate_per_kwh_cents, with no rounding of its own
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2073 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2073. Noise review: repeated reads traced to a flapping collector, suppressed at the source.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2074 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2074. Quarterly access recertification touched this district; no biller-relevant configuration changed.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2075 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2075. Capacity review noted rising consumption; thresholds unchanged outside the governance process.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2076 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2076. Route-book resequencing drill completed; read acknowledgment stayed within the governance service level.
> **Governance decision (2026-04-06 - #TAR-7320)** Marek: demand ratchet, final: process each account's bills in ascending (period_start, period_end, read_id) order. ratchet_floor_kw = ceil(highest METERED peak_demand_kw over that account's previous ratchet_lookback_periods bills * ratchet_percent / 100), and 0 when the account has no earlier bill. It is the metered peak that carries forward, never the billed demand, so a ratcheted period does not re-ratchet the next one -- this revises #TAR-7220. billed_demand_kw = max(peak_demand_kw, ratchet_floor_kw) and ratchet_uplift_kw = billed_demand_kw - peak_demand_kw. ROUNDING: ratchet floor = CEIL
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2077 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2077. Change-board reviewed stale exception approvals; owners pinged before the next billing cycle.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2078 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2078. Rate-set rollback rehearsal ran clean; no changes to biller parameters were approved.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2079 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2079. Vendor ticket on collector retries closed; delivery within contractual budget.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2080 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2080. Meter-to-cash dashboard tiles lagged during the rate refresh; attributed to cache staleness, not the biller.
> **Governance decision (2026-04-06 - #TAR-7322)** Marek: capacity charge, final: demand_charge_cents is summed over segments as billed_demand_kw * demand_rate_cents_per_kw * segment_days // billed_days, taking the rate from the schedule version and governing class of that segment. Each segment's term is floored on its own, superseding the rounding-up of #TAR-7222. ROUNDING: segment capacity charge = FLOOR
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2081 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2081. Docket exhibit audit sampled cross-account roles; no biller-relevant findings for this district.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2082 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2082. Synthetic read injection verified bill delivery to the print vendor for this district.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2083 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2083. Noise review: repeated reads traced to a flapping collector, suppressed at the source.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2084 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2084. Quarterly access recertification touched this district; no biller-relevant configuration changed.
> **Governance decision (2026-04-06 - #TAR-7324)** Marek: standing charge, final: standing_charge_cents is the exact sum over segments of segment_days * standing_charge_cents_per_day for that segment's schedule version and governing class. It carries no rounding and is never prorated a second time
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2085 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2085. Capacity review noted rising consumption; thresholds unchanged outside the governance process.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2086 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2086. Route-book resequencing drill completed; read acknowledgment stayed within the governance service level.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2087 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2087. Change-board reviewed stale exception approvals; owners pinged before the next billing cycle.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2088 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2088. Rate-set rollback rehearsal ran clean; no changes to biller parameters were approved.
> **Governance decision (2026-04-08 - #TAR-7330)** Priya: service-class precedence, final: for each segment the governing class is the account's entry in /app/data/service_class_register.json whose effective_from is the latest one on or before that segment's first day; only when the register holds no entry in force for the account, or names a class the schedule version does not carry, does the class declared on the meter read govern; and only when that too is absent or unknown is the account billed as residential. This supersedes #TAR-7212, under which the declared class always won. The bill's own service_class -- the one reported and the one its policy resolves against -- is the governing class of the LAST segment
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2089 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2089. Vendor ticket on collector retries closed; delivery within contractual budget.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2090 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2090. Meter-to-cash dashboard tiles lagged during the rate refresh; attributed to cache staleness, not the biller.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2091 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2091. Docket exhibit audit sampled cross-account roles; no biller-relevant findings for this district.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2092 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2092. Synthetic read injection verified bill delivery to the print vendor for this district.
> **Governance decision (2026-04-10 - #TAR-7340)** Priya: minimum bill, final: subtotal_cents = energy_charge_cents + demand_charge_cents + standing_charge_cents. The floor prorates to the period as round_half_up(minimum_bill_cents * billed_days / minimum_bill_days_basis), i.e. add half the basis before the integer division. minimum_applied is true only when subtotal_cents is STRICTLY below that prorated floor, in which case billed_subtotal_cents is the floor; otherwise billed_subtotal_cents is subtotal_cents. This supersedes the floored proration of #TAR-7228. ROUNDING: prorated minimum bill = HALF UP
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2093 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2093. Noise review: repeated reads traced to a flapping collector, suppressed at the source.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2094 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2094. Quarterly access recertification touched this district; no biller-relevant configuration changed.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2095 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2095. Capacity review noted rising consumption; thresholds unchanged outside the governance process.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2096 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2096. Route-book resequencing drill completed; read acknowledgment stayed within the governance service level.
> **Governance decision (2026-04-10 - #TAR-7342)** Priya: statutory levy, final: levy_cents = billed_subtotal_cents * levy_bps // 10000, charged on the subtotal AFTER any minimum-bill floor has been applied, not on the metered subtotal as #TAR-7228 had it. total_due_cents = billed_subtotal_cents + levy_cents. ROUNDING: levy = FLOOR
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2097 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2097. Change-board reviewed stale exception approvals; owners pinged before the next billing cycle.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2098 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2098. Rate-set rollback rehearsal ran clean; no changes to biller parameters were approved.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2099 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2099. Vendor ticket on collector retries closed; delivery within contractual budget.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2100 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2100. Meter-to-cash dashboard tiles lagged during the rate refresh; attributed to cache staleness, not the biller.
> **Governance decision (2026-04-12 - #TAR-7350)** Marek: exception_score = (total_due_cents // 2500) + (ratchet_uplift_kw // 6) + max(bracket_span - 1, 0), where bracket_span is the number of distinct bracket_ids that received a non-zero share of the read across all of the bill's segments and bracket_ids lists those identifiers ascending. Both divisions FLOOR. This supersedes #TAR-7240. ROUNDING: total_due_cents // 2500 = FLOOR. ROUNDING: ratchet_uplift_kw // 6 = FLOOR
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2101 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2101. Docket exhibit audit sampled cross-account roles; no biller-relevant findings for this district.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2102 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2102. Synthetic read injection verified bill delivery to the print vendor for this district.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2103 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2103. Noise review: repeated reads traced to a flapping collector, suppressed at the source.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2104 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2104. Quarterly access recertification touched this district; no biller-relevant configuration changed.
> **Governance decision (2026-04-12 - #TAR-7352)** Marek: exception admission: a bill enters the exception queue iff its exception_score is at least the admission_min resolved for its own service class (inclusive: equal to the floor admits) OR its minimum_applied flag is set, since a bill the floor lifted is a regulatory exception however small it is. Every bill is written to the bill register whether or not it is admitted
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2105 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2105. Capacity review noted rising consumption; thresholds unchanged outside the governance process.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2106 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2106. Route-book resequencing drill completed; read acknowledgment stayed within the governance service level.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2107 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2107. Change-board reviewed stale exception approvals; owners pinged before the next billing cycle.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2108 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2108. Rate-set rollback rehearsal ran clean; no changes to biller parameters were approved.
> **Governance decision (2026-04-14 - #TAR-7354)** Marek: tier assignment (thresholds are resolved policy values): a bill is escalate iff total_due_cents >= escalate_total_cents OR exception_score >= escalate_score_min OR ratchet_uplift_kw >= escalate_ratchet_min. Otherwise, evaluated only when escalate does not hold, review iff exception_score >= review_score_min OR segment_count >= review_segment_min OR minimum_applied OR bracket_span >= review_bracket_min. Otherwise watch. This supersedes #TAR-7244
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2109 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2109. Vendor ticket on collector retries closed; delivery within contractual budget.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2110 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2110. Meter-to-cash dashboard tiles lagged during the rate refresh; attributed to cache staleness, not the biller.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2111 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2111. Docket exhibit audit sampled cross-account roles; no biller-relevant findings for this district.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2112 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2112. Synthetic read injection verified bill delivery to the print vendor for this district.
> **Governance decision (2026-04-14 - #TAR-7356)** Yusuf: final queue ordering, strictly in sequence: tier rank escalate > review > watch; then exception_score desc; then total_due_cents desc; then energy_charge_cents desc; then billed_demand_kw desc; then consumption_kwh desc; then account asc; then period_start asc; then read_id asc
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2113 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2113. Noise review: repeated reads traced to a flapping collector, suppressed at the source.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2114 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2114. Quarterly access recertification touched this district; no biller-relevant configuration changed.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2115 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2115. Capacity review noted rising consumption; thresholds unchanged outside the governance process.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2116 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2116. Route-book resequencing drill completed; read acknowledgment stayed within the governance service level.
> **Governance decision (2026-04-16 - #TAR-7358)** Yusuf: inspector capacity cap: at most TWO exception-queue rows per account. The cap is a FINAL pass over the fully ordered queue (not applied during admission and not per account before ordering): admit and prioritise every bill, apply the #TAR-7356 ordering, then walk the ordered queue from the top keeping the first two rows of each account and discarding the rest. Which rows survive depends on the global order, so a bill ranked third within its account is dropped even if it outranks a retained row from another account. Discarded rows do not contribute to any queue-derived summary field
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2117 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2117. Change-board reviewed stale exception approvals; owners pinged before the next billing cycle.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2118 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2118. Rate-set rollback rehearsal ran clean; no changes to biller parameters were approved.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2119 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2119. Vendor ticket on collector retries closed; delivery within contractual budget.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2120 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2120. Meter-to-cash dashboard tiles lagged during the rate refresh; attributed to cache staleness, not the biller.
> **Governance decision (2026-04-18 - #TAR-7360)** Lena: billing policy baseline (read from /app/data/billing_policies.json at that fixed absolute path; --input never relocates it). Any field the policy file omits keeps its baseline: admission_min = 240; escalate_total_cents = 1870000; escalate_score_min = 780; escalate_ratchet_min = 540; review_score_min = 430; review_bracket_min = 5; review_segment_min = 27; minimum_bill_cents = 1800; minimum_bill_days_basis = 30; ratchet_percent = 80; ratchet_lookback_periods = 3; levy_bps = 240
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2121 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2121. Docket exhibit audit sampled cross-account roles; no biller-relevant findings for this district.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2122 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2122. Synthetic read injection verified bill delivery to the print vendor for this district.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2123 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2123. Noise review: repeated reads traced to a flapping collector, suppressed at the source.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2124 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2124. Quarterly access recertification touched this district; no biller-relevant configuration changed.
> **Governance decision (2026-04-18 - #TAR-7362)** Lena: policy resolution, per service class, in three layers: start from the #TAR-7360 baseline; overlay every field the policy file's `default` object supplies (it need not be complete -- an omitted field keeps its baseline); then overlay every field that class's entry in `class_overrides` supplies (an override names only the fields it changes and inherits the rest). Coerce every policy value to int. A bill resolves its policy against the service_class fixed by #TAR-7330
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2125 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2125. Capacity review noted rising consumption; thresholds unchanged outside the governance process.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2126 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2126. Route-book resequencing drill completed; read acknowledgment stayed within the governance service level.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2127 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2127. Change-board reviewed stale exception approvals; owners pinged before the next billing cycle.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2128 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2128. Rate-set rollback rehearsal ran clean; no changes to biller parameters were approved.
> **Governance decision (2026-04-19 - #TAR-7364)** Yusuf: summary aggregation domains: max_exception_score, max_total_due_cents and max_ratchet_uplift_kw are maxima over the FINAL admitted exception_queue rows only, using 0 when the queue is empty. Only largest_bill_cents is taken over EVERY bill in the register, admitted or not, using 0 when there are no bills. The total_* fields, minimum_applied_count, estimated_bill_count, account_count and bill_count are likewise taken over every bill; schedule_version_count is the number of schedule versions in the consolidated rate table
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2129 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2129. Vendor ticket on collector retries closed; delivery within contractual budget.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2130 — eastgate (district 11) route
Billing supervisor logged a routine observation for eastgate (district 11) during billing cycle 2130. Meter-to-cash dashboard tiles lagged during the rate refresh; attributed to cache staleness, not the biller.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2131 — millbrook (district 6) route
Billing supervisor logged a routine observation for millbrook (district 6) during billing cycle 2131. Docket exhibit audit sampled cross-account roles; no biller-relevant findings for this district.
No biller semantics changed in this entry; parameters remain as approved by the commission.

### Review entry 2132 — riverside (district 4) route
Billing supervisor logged a routine observation for riverside (district 4) during billing cycle 2132. Synthetic read injection verified bill delivery to the print vendor for this district.
> **Governance decision (2026-05-04 - #TAR-7370)** Lena: authoritative rate-table consolidation, final -- this supersedes the #TAR-7208 draft and revises the #TAR-7231 interim, and it runs BEFORE any bill is issued. The shipped `/app/data/effective_rate_table.json` fell behind the docket and is no longer authoritative; it must be rebuilt in place from the two filed sources beside it. Consolidate only filings whose status is `approved`: a `withdrawn` or `pending` filing has no force and contributes nothing, not even a schedule version of its own (this revises #TAR-7231, which consolidated pending filings). Order the approved filings by effective_date ascending, then filed_on ascending, then filing_id ascending -- two filings sharing an effective_date are settled by which was filed later, and filing_id only breaks a remaining tie (this revises #TAR-7231's filed_on-only ordering and #TAR-7208's file order). Start from `/app/data/base_tariff.json` and apply the filings in that order, cumulatively: `replace-bracket` and `add-bracket` both write the filed bracket over any bracket already carrying that bracket_id in that service class and otherwise insert it, so a later filing supersedes an earlier one for the same bracket; `retire-bracket` removes the named bracket from that class; `adjust-demand-charge` sets that class's demand_rate_cents_per_kw. A retirement is NOT permanent: a later add filing naming a retired bracket_id reinstates it with the filed ceiling and rate, revising #TAR-7231. Emit one schedule version per DISTINCT effective_date among the approved filings, plus one for the base tariff's own effective_from, each carrying the cumulative state of the tariff on that date; a filing dated before the base effective_from folds into the base version. Schedules are ordered by effective_from ascending, class keys ascending, and each class's brackets ascending by upper_kwh with the unbounded bracket last and remaining ties by bracket_id. filing_id, docket, filed_on, effective_date, status, operation and rationale are filing bookkeeping, not tariff fields: the consolidated table carries exactly tariff_id and schedules, a schedule exactly effective_from and classes, a class exactly brackets, demand_rate_cents_per_kw and standing_charge_cents_per_day, and a bracket exactly bracket_id, upper_kwh and rate_per_kwh_cents. Write the result back to `/app/data/effective_rate_table.json`. Nothing downstream re-derives it -- every proration boundary and every rate the biller charges is read from this table -- so a table consolidated any other way yields wrong bills
Reviewers should reconcile behaviour questions against #TAR governance decisions rather than chat excerpts.

### Review entry 2133 — harbour (district 9) route
Billing supervisor logged a routine observation for harbour (district 9) during billing cycle 2133. Noise review: repeated reads traced to a flapping collector, suppressed at the source.
Thread archived; see the #TAR decision entries for anything affecting biller behaviour.

### Review entry 2134 — northfield (district 2) route
Billing supervisor logged a routine observation for northfield (district 2) during billing cycle 2134. Quarterly access recertification touched this district; no biller-relevant configuration changed.
Historical spreadsheet exports remain archived and non-authoritative for the itemised bill acceptance.

### Review entry 2135 — old town (district 7) route
Billing supervisor logged a routine observation for old town (district 7) during billing cycle 2135. Capacity review noted rising consumption; thresholds unchanged outside the governance process.
No biller semantics changed in this entry; parameters remain as approved by the commission.
