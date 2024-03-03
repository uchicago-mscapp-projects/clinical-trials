DROP TABLE IF EXISTS TRIALS_JOINED;

CREATE TABLE TRIALS_JOINED AS SELECT 
ti.nct_id
, ti.INTERVENTION_NAME
, tr.LEAD_SPONSOR
FROM 
trials tr
INNER JOIN trial_interventions ti on tr.nct_id = ti.nct_id;