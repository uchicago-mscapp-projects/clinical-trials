"""
Collection of header mappings used to rename dataframes for loading to
SQL tables
"""

trials_headers = {
 'protocolSection.identificationModule.nctId': 'nct_id',
 'protocolSection.identificationModule.orgStudyIdInfo.id': 'org_study_id_info',
 'protocolSection.identificationModule.secondaryIdInfos': 'secondary_id_infos',
 'protocolSection.identificationModule.organization.fullName': 'org_full_name',
 'protocolSection.identificationModule.organization.class': 'org_class',
 'protocolSection.identificationModule.briefTitle': 'brief_title',
 'protocolSection.identificationModule.officialTitle': 'official_title'
 }

status_headers = {
'protocolSection.identificationModule.nctId': 'nct_id',
 'protocolSection.statusModule.statusVerifiedDate': 'status_verified_date',
 'protocolSection.statusModule.overallStatus': 'overall_status',
 'protocolSection.statusModule.expandedAccessInfo.hasExpandedAccess': \
    'has_expanded_access',
 'protocolSection.statusModule.startDateStruct.date': 'start_date',
 'protocolSection.statusModule.primaryCompletionDateStruct.date': \
    'primary_completion_date',
 'protocolSection.statusModule.primaryCompletionDateStruct.type': \
    'primary_completion_date_type',
 'protocolSection.statusModule.completionDateStruct.date': 'completion_date',
 'protocolSection.statusModule.completionDateStruct.type': \
    'completion_date_type',
 'protocolSection.statusModule.studyFirstSubmitDate': 'first_submit_date',
 'protocolSection.statusModule.studyFirstSubmitQcDate': \
    'first_submit_qc_date',
 'protocolSection.statusModule.studyFirstPostDateStruct.date': \
    'first_post_date',
 'protocolSection.statusModule.studyFirstPostDateStruct.type': \
    'first_post_date_type',
 'protocolSection.statusModule.resultsFirstSubmitDate': \
    'results_first_submit_date',
 'protocolSection.statusModule.resultsFirstSubmitQcDate': \
    'results_first_submit_qc_date',
 'protocolSection.statusModule.resultsFirstPostDateStruct.date': \
    'results_first_post_date',
 'protocolSection.statusModule.resultsFirstPostDateStruct.type': \
    'results_first_post_date_type',
 'protocolSection.statusModule.lastUpdateSubmitDate': \
    'last_update_submit_date',
 'protocolSection.statusModule.lastUpdatePostDateStruct.date': \
    'last_update_post_date',
 'protocolSection.statusModule.lastUpdatePostDateStruct.type': \
    'last_update_post_date_type',
 'protocolSection.statusModule.startDateStruct.type': \
    'start_date_type',
 'protocolSection.statusModule.dispFirstSubmitDate': \
    'disp_first_submit_date',
 'protocolSection.statusModule.dispFirstSubmitQcDate': \
    'disp_first_submit_qc_date',
 'protocolSection.statusModule.dispFirstPostDateStruct.date': \
    'disp_first_post_date',
 'protocolSection.statusModule.dispFirstPostDateStruct.type': \
    'disp_first_post_date_type',
 'protocolSection.statusModule.lastKnownStatus': \
    'last_known_status',
 'protocolSection.statusModule.whyStopped': 'why_stopped'
}

conditions_headers = {
    'protocolSection.identificationModule.nctId': 'nct_id',
    'protocolSection.conditionsModule.conditions': 'conditions',
    'derivedSection.conditionBrowseModule.meshes': 'meshes',
    'derivedSection.conditionBrowseModule.ancestors': 'ancestors',
    'protocolSection.conditionsModule.keywords': 'keywords'
}

baseline_headers = {
'protocolSection.identificationModule.nctId': 'nct_id',
'resultsSection.baselineCharacteristicsModule.measures': 'measures'
}

interventions_headers = {
    'protocolSection.identificationModule.nctId': 'nct_id',
    'protocolSection.armsInterventionsModule.armGroups': 'arm_groups',
    'protocolSection.armsInterventionsModule.interventions': 'interventions'
}