SELECT
  patients.*,
  codes.all_diagnosis_codes
FROM patients
LEFT JOIN (
    SELECT member_id,
    sort_array(
        collect_list(
                struct(
                    diagnosis.diagnosis_id,
                    diagnosis.icd_code,
                    icd_lookup.icd_description
                    )
                )
            ) as all_diagnosis_codes
    FROM diagnosis
    LEFT OUTER JOIN icd_lookup
        ON diagnosis.icd_code = icd_lookup.icd_code
    GROUP BY member_id
) codes
ON codes.member_id = patients.member_id