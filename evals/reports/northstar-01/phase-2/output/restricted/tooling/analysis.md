# Analysis scope and interpretation

The helper processes an already-scored matrix for one exact form and item revision set. It does not judge practical responses or authenticate candidate participation. Preserve the source dataset, scoring policy, cohort selection, form fingerprint, exclusions and analyst decisions alongside the report.

## Calculations

- Total score: sum of the supplied item scores; no implicit rescaling, weighting, imputation or rounding.
- Item mean proportion: mean score divided by item maximum. For dichotomous items it is proportion correct. For practical items it is a score proportion, not a probability of a correct response.
- Corrected item-total association: Pearson correlation of the item score with total minus that item score, calculated on all supplied rows. For dichotomous items this is the corrected point-biserial correlation. Undefined when either variable has no variance or there are fewer than two observations.
- Coefficient alpha: `k/(k-1) * (1 - sum(sample item variances)/sample total variance)`. Undefined with fewer than two people/items or zero total variance. Negative results are retained, not clamped into a reassuring range. This statistic alone does not establish unidimensionality, validity, fairness or decision consistency.
- Expected-score panel summary: each judge's expected item scores are summed; totals are averaged. This arithmetic may support the selected procedure, but it does not establish panel suitability, method suitability, a passing standard, or a rounding policy.

The complete-case input contract rejects missing scores so an omission policy cannot be silently invented. Report the cohort size and its limits; no universal sample minimum or statistic threshold makes an item acceptable. High/low values prompt review in context. Small or unrepresentative samples remain small or unrepresentative even when a calculation succeeds.

## Unsupported conclusions

No automatic item removal, pass/fail decisions, IRT fit, DIF analysis, test equating, subgroup fairness conclusion, standard error near a decision threshold, inter-rater agreement, legal compliance or accreditation determination is implemented. If requested, specify the study question, data, assumptions and suitable tool/expert handoff. Do not replace missing analyses with invented numbers or treat similar average subgroup scores as proof of fairness.

## References

[Standards for Educational and Psychological Testing](https://www.testingstandards.net/uploads/7/6/6/4/76643089/standards_2014edition.pdf) provides the professional framework for score interpretations, evidence and intended uses; [NCCA FAQs](https://www.credentialingexcellence.org/Accreditation/Earn-Accreditation/NCCA/FAQs) discusses job analysis and specifications. These links are references, not claims of accreditation or compliance. Recheck current applicable guidance for a real program.
