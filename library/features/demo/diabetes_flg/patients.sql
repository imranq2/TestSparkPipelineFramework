SELECT
    patients.*,
    CASE
      WHEN exists(all_diagnosis_codes, x -> x.icd_code IN (
              'E10.10',
              'E08.43'
)) THEN 1
      ELSE 0
    END AS diabetes_flg
FROM patients