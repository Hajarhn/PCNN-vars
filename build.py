#!/usr/bin/env python3
"""Generate PCNN variable vocabulary files."""
from pathlib import Path
import csv
import html

ROOT = Path(__file__).parent
DOCS = ROOT / "docs"
DOCS.mkdir(exist_ok=True)

NS = "https://w3id.org/pcnn/"
VAR = NS + "var/"
VS = NS + "vs/"

# Shared value sets: id -> list of (code, en)
VALUE_SETS = {
    "dsq-freq-0-4": [
        ("0", "none of the time"),
        ("1", "a little of the time"),
        ("2", "about half the time"),
        ("3", "most of the time"),
        ("4", "all of the time"),
    ],
    "dsq-sev-1-4": [
        ("1", "mild"),
        ("2", "moderate"),
        ("3", "severe"),
        ("4", "very severe"),
    ],
    "cis-1-7": [
        ("1", "yes, that is true"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "no, that is not true"),
    ],
    "yes-no": [("1", "Yes"), ("0", "No")],
    "yes-no-unknown": [("1", "Yes"), ("0", "No"), ("3", "I don't know")],
    "yes-no-recovered": [
        ("1", "Yes"),
        ("0", "No"),
        ("3", "Not anymore, I have recovered"),
    ],
    "smokingstatus-6": [
        ("1", "No"),
        ("2", "No, but I have smoked in the past"),
        ("3", "Yes, occasionally"),
        ("4", "Daily, less than 10 cigarettes/cigars per day"),
        ("5", "Daily, 10 or more cigarettes/cigars per day"),
        ("6", "Daily, e-cigarettes/vapes only"),
    ],
    "paidjob-4": [
        ("1", "Yes"),
        ("0", "No"),
        ("3", "Yes, but I have been reported sick (partly) due to long-term complaints"),
        ("4", "No, I no longer have a job due to long-term complaints"),
    ],
    "income-13": [
        ("1", "I do not know"),
        ("2", "I rather not answer"),
        ("3", "Less than EUR 750"),
        ("4", "EUR 750 - 1000"),
        ("5", "EUR 1000 - 1500"),
        ("6", "EUR 1500 - 2000"),
        ("7", "EUR 2000 - 2500"),
        ("8", "EUR 2500 - 3000"),
        ("9", "EUR 3000 - 3500"),
        ("10", "EUR 3500 - 4000"),
        ("11", "EUR 4000 - 4500"),
        ("12", "EUR 4500 - 5000"),
        ("13", "more than EUR 5000"),
    ],
    "employment-10": [
        ("1", "Paid job 32 hours or more per week"),
        ("2", "Paid job 20 to less than 32 hours per week"),
        ("3", "Paid job 12 to less than 20 hours per week"),
        ("4", "Paid job less than 12 hours per week"),
        ("5", "Retired (early retirement / AOW / VUT / FPU)"),
        ("6", "Unemployed / jobseeker"),
        ("7", "Work disabled (WAO / AAW / WAZ / Wajong)"),
        ("8", "Receiving a social security benefit"),
        ("9", "Full-time homemaker"),
        ("10", "In education / study"),
    ],
    "bpi-front-26": [
        ("1", "No pain"),
        ("2", "Face"),
        ("3", "Right jaw"),
        ("4", "Left jaw"),
        ("5", "Right chest"),
        ("6", "Left chest"),
        ("7", "Right upper arm"),
        ("8", "Left upper arm"),
        ("9", "Right elbow"),
        ("10", "Left elbow"),
        ("11", "Abdomen"),
        ("12", "Pelvis"),
        ("13", "Right forearm"),
        ("14", "Left forearm"),
        ("15", "Right wrist/hand"),
        ("16", "Left wrist/hand"),
        ("17", "Right groin"),
        ("18", "Left groin"),
        ("19", "Right thigh"),
        ("20", "Left thigh"),
        ("21", "Right knee"),
        ("22", "Left knee"),
        ("23", "Right lower leg"),
        ("24", "Left lower leg"),
        ("25", "Right ankle/foot"),
        ("26", "Left ankle/foot"),
    ],
    "bpi-interfere-0-10": [
        ("0", "no interference"),
        ("1", "1"),
        ("2", "2"),
        ("3", "3"),
        ("4", "4"),
        ("5", "5"),
        ("6", "6"),
        ("7", "7"),
        ("8", "8"),
        ("9", "9"),
        ("10", "complete interference"),
    ],
    "onbehalf-8": [
        ("1", "Parent or legal guardian"),
        ("2", "Child"),
        ("3", "Sibling"),
        ("4", "Partner"),
        ("5", "Other relative"),
        ("6", "Friend"),
        ("7", "Care giver (not family)"),
        ("8", "Other"),
    ],
    "howheard-7": [
        ("1", "Via my GP"),
        ("2", "Via the media (free text)"),
        ("3", "Via friends or family"),
        ("4", "Via Thuisarts.nl"),
        ("5", "Via Google or another search engine"),
        ("6", "Invitation by letter/email"),
        ("7", "Other (free text)"),
    ],
    "invitation-3": [
        ("1", "Invitation after RIVM long-COVID study"),
        ("2", "Invitation via C-support"),
        ("3", "Via the RECLAIM newsletter"),
    ],
    "hospital-treat-3": [
        ("1", "Admitted to ICU"),
        ("2", "Received oxygen"),
        ("3", "Neither"),
    ],
    "pos-test-type-5": [
        ("1", "PCR or antigen rapid test taken by an expert"),
        ("2", "Blood test (serology)"),
        ("3", "Self-test"),
        ("4", "Diagnosed by treating physician; test type unknown"),
        ("5", "I do not know"),
    ],
    "pc-confirmedby-6": [
        ("1", "A general practitioner"),
        ("2", "A medical specialist"),
        ("3", "An alternative practitioner"),
        ("4", "People who know me well think I have it; not officially confirmed"),
        ("5", "I think I have it myself; not officially confirmed"),
        ("6", "Other (free text)"),
    ],
    "permission-2": [
        ("1", "Yes, I may be approached; contact details provided"),
        ("0", "No, questionnaire study only"),
    ],
    "travel-3": [
        ("1", "Yes"),
        ("2", "Yes, but not longer than 1 hour"),
        ("0", "No"),
    ],
    "s31-skin-2": [("1", "My hands"), ("2", "My feet")],
    "depression-history": [("1", "Yes, last in year ..."), ("0", "No")],
    "vaccin-ltc-other": [("1", "Yes, namely: free text"), ("0", "No")],
    "permissions-check": [("1", "Yes, this is correct")],
    "c31-dry-mouth": [("1", "Yes"), ("0", "No")],
}

# column, theme, instrument, label_en, definition, datatype, valueset, unit, map_rel, map_uri, map_note
VARS = [
    ("smokingstatus", "demographics / lifestyle", "none", "Do you smoke?",
     "Self-reported current smoking behaviour, including former smoking, occasional use, daily tobacco use by amount, and exclusive e-cigarette or vape use.",
     "coded", "smokingstatus-6", "", "closeMatch", "http://loinc.org/72166-2",
     "Same topic as LOINC 72166-2; PCNN uses a 6-level list including vapes."),
    ("paidjob", "demographics / work", "none", "Do you have a paid job at this moment?",
     "Whether the respondent currently has paid work, including partial sick leave and job loss due to long-term complaints.",
     "coded", "paidjob-4", "", "relatedMatch", "http://purl.obolibrary.org/obo/NCIT_C95551",
     "Employment-related concept only; response options are PCNN-specific."),
    ("hours_household", "demographics / activity", "none", "Household activities (hours per week)",
     "Hours per week spent on household activities.",
     "number", "", "h/wk", "relatedMatch", "http://loinc.org/57253-7",
     "Not the same item. LOINC 57253-7 is OASIS-C functional independence, not hours per week."),
    ("hours_family", "demographics / activity", "none", "Family activities (hours per week)",
     "Hours per week spent on family activities.",
     "number", "", "h/wk", "relatedMatch", "", "No suitable exact public item found."),
    ("dsq_fatigue_freq", "symptoms / frequency", "DSQ", "Frequency past 6 months: Fatigue / extreme tiredness",
     "DSQ frequency rating for fatigue or extreme tiredness over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://snomed.info/id/84229001",
     "SNOMED fatigue is the symptom, not this DSQ frequency item."),
    ("dsq_slowspeech_sev", "symptoms / severity", "DSQ-2", "Severity past 6 months: Slowed speech",
     "DSQ-2 severity rating for slowed speech over the past 6 months.",
     "coded", "dsq-sev-1-4", "", "", "", "No public item IRI found for this DSQ-2 item."),
    ("dsq_memory_freq", "symptoms / frequency", "DSQ-SF + DSQ-2", "Frequency past 6 months: Problems remembering things",
     "DSQ frequency rating for problems remembering things over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://snomed.info/id/386807006",
     "SNOMED memory concept is the symptom, not the DSQ frequency item."),
    ("dsq_exhausted_freq", "symptoms / frequency / PEM", "DSQ-PEM + DSQ-2", "Frequency past 6 months: Physically drained or sick after mild activity",
     "DSQ frequency rating for feeling physically drained or sick after mild activity over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://snomed.info/id/84229001", ""),
    ("dsq_heavy_freq", "symptoms / frequency / PEM", "DSQ-SF + DSQ-PEM + DSQ-2", "Frequency past 6 months: Dead, heavy feeling after starting to exercise",
     "DSQ frequency rating for a dead, heavy feeling after starting to exercise over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://snomed.info/id/161874006", ""),
    ("dsq_muscletwitch_freq", "symptoms / frequency", "DSQ-2", "Frequency past 6 months: Muscle twitches",
     "DSQ-2 frequency rating for muscle twitches over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "", "", "No public item IRI found."),
    ("dsq_muscletwitch_sev", "symptoms / severity", "DSQ-2", "Severity past 6 months: Muscle twitches",
     "DSQ-2 severity rating for muscle twitches over the past 6 months.",
     "coded", "dsq-sev-1-4", "", "", "", "No public item IRI found."),
    ("dsq_soreness_freq", "symptoms / frequency / PEM", "DSQ-SF + DSQ-PEM + DSQ-2", "Frequency past 6 months: Next-day soreness or fatigue after non-strenuous everyday activities",
     "DSQ frequency rating for next-day soreness or fatigue after non-strenuous everyday activities.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://snomed.info/id/71393004", ""),
    ("dsq_minexercise_sev", "symptoms / severity / PEM", "DSQ-SF + DSQ-PEM + DSQ-2", "Severity past 6 months: Minimum exercise makes you physically tired",
     "DSQ severity rating for becoming physically tired after minimum exercise.",
     "coded", "dsq-sev-1-4", "", "relatedMatch", "http://snomed.info/id/408578001", ""),
    ("dsq_pain_freq", "symptoms / frequency", "DSQ-SF + DSQ-2", "Frequency past 6 months: Pain or aching in your muscles",
     "DSQ frequency rating for muscle pain or aching over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://snomed.info/id/68962001", ""),
    ("dsq_forgetful_freq", "symptoms / frequency", "DSQ-2", "Frequency past 6 months: Absent-mindedness or forgetfulness",
     "DSQ-2 frequency rating for absent-mindedness or forgetfulness over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "", "", "No public item IRI found."),
    ("dsq_shortbreath_freq", "symptoms / frequency", "DSQ-2", "Frequency past 6 months: Shortness of breath",
     "DSQ-2 frequency rating for shortness of breath or trouble catching breath over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "", "", "No public item IRI found."),
    ("dsq_noappetite_freq", "symptoms / frequency", "DSQ-2", "Frequency past 6 months: No appetite",
     "DSQ-2 frequency rating for no appetite over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "", "", "No public item IRI found."),
    ("dsq_unablestand_freq", "symptoms / frequency / POTS", "DSQ-POTS + DSQ-2", "Frequency past 6 months: Inability to tolerate an upright position",
     "DSQ frequency rating for inability to tolerate an upright position over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://snomed.info/id/870368003", ""),
    ("dsq_bloating_freq", "symptoms / frequency", "DSQ-SF + DSQ-2", "Frequency past 6 months: Bloating",
     "DSQ frequency rating for bloating over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://snomed.info/id/116289008", ""),
    ("dsq_slowthink_freq", "symptoms / frequency", "DSQ-2", "Frequency past 6 months: Slowness of thought",
     "DSQ-2 frequency rating for slowness of thought over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "", "", "No public item IRI found."),
    ("dsq_ibs_freq", "symptoms / frequency", "DSQ-SF + DSQ-2", "Frequency past 6 months: Irritable bowel problems",
     "DSQ frequency rating for irritable bowel problems over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://snomed.info/id/10743008", ""),
    ("dsq_irregularhb_freq", "symptoms / frequency / POTS", "DSQ-2", "Frequency past 6 months: Irregular heart beats",
     "DSQ-2 frequency rating for irregular heart beats over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://purl.obolibrary.org/obo/NCIT_C168414", ""),
    ("dsq_lowtemp_freq", "symptoms / frequency", "DSQ-2", "Frequency past 6 months: Feeling like you have a low temperature",
     "DSQ-2 frequency rating for feeling as if body temperature is low.",
     "coded", "dsq-freq-0-4", "", "", "", "No public item IRI found."),
    ("dsq_flu_freq", "symptoms / frequency", "DSQ-SF + DSQ-2", "Frequency past 6 months: Flu-like symptoms",
     "DSQ frequency rating for flu-like symptoms over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://purl.obolibrary.org/obo/NCIT_C143492", ""),
    ("dsq_nightawake_freq", "symptoms / frequency", "DSQ-2", "Frequency past 6 months: Sleeping all day and staying awake all night",
     "DSQ-2 frequency rating for sleeping all day and staying awake all night.",
     "coded", "dsq-freq-0-4", "", "", "", "No public item IRI found."),
    ("dsq_dizzy_freq", "symptoms / frequency / POTS", "DSQ-2", "Frequency past 6 months: Dizziness or fainting",
     "DSQ-2 frequency rating for dizziness or fainting over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://loinc.org/69712-8", ""),
    ("dsq_hightemp_freq", "symptoms / frequency", "DSQ-2", "Frequency past 6 months: Feeling like you have a high temperature",
     "DSQ-2 frequency rating for feeling as if body temperature is high.",
     "coded", "dsq-freq-0-4", "", "", "", "No public item IRI found."),
    ("dsq_coldlimbs_freq", "symptoms / frequency", "DSQ-SF + DSQ-2", "Frequency past 6 months: Cold limbs",
     "DSQ frequency rating for cold arms, legs, hands or feet over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://snomed.info/id/771542000", ""),
    ("dsq_sensitivities_freq", "symptoms / frequency", "DSQ-SF + DSQ-2", "Frequency past 6 months: Some smells, foods, medications or chemicals make you feel sick",
     "DSQ frequency rating for feeling sick from some smells, foods, medications or chemicals.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://snomed.info/id/16932000", ""),
    ("dsq_musclefatigue_sev", "symptoms / severity / PEM", "DSQ-2", "Severity past 6 months: Muscle fatigue after mild physical activity",
     "DSQ-2 severity rating for muscle fatigue after mild physical activity.",
     "coded", "dsq-sev-1-4", "", "relatedMatch", "http://purl.obolibrary.org/obo/NCIT_C189011", ""),
    ("dsq_pressurepain_freq", "symptoms / frequency", "DSQ-2", "Frequency past 6 months: Pressure on parts of the body causes pain in other parts",
     "DSQ-2 frequency rating for pain referred from pressure on other body parts.",
     "coded", "dsq-freq-0-4", "", "", "", "No public item IRI found."),
    ("dsq_blackedvision_freq", "symptoms / frequency / POTS", "DSQ-POTS + DSQ-2", "Frequency past 6 months: Graying or blacking out after standing",
     "DSQ frequency rating for graying or blacking out after standing.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://loinc.org/69712-8", ""),
    ("dsq_pemphysical_freq", "symptoms / frequency / PEM", "DSQ-PEM + DSQ-2", "Frequency past 6 months: Worsening of symptoms after mild physical activity",
     "DSQ frequency rating for worsening of symptoms after mild physical activity.",
     "coded", "dsq-freq-0-4", "", "relatedMatch", "http://purl.obolibrary.org/obo/NCIT_C189011", ""),
    ("dsq_achingeyes_freq", "symptoms / frequency", "DSQ-2", "Frequency past 6 months: Aching of the eyes or behind the eyes",
     "DSQ-2 frequency rating for aching of the eyes or behind the eyes.",
     "coded", "dsq-freq-0-4", "", "", "", "No public item IRI found."),
    ("dsq_headache_freq", "symptoms / frequency", "DSQ-2", "Frequency past 6 months: Headaches",
     "DSQ-2 frequency rating for headaches over the past 6 months.",
     "coded", "dsq-freq-0-4", "", "", "", "No public item IRI found."),
    ("bpi_pain_where_front", "pain", "Brief Pain Inventory", "Indicate your main pain area (front)",
     "Main pain region selected on the front body map of the Brief Pain Inventory.",
     "coded", "bpi-front-26", "", "relatedMatch", "", "BPI body-map item; regions are instrument-specific."),
    ("bpi_prohibited_activity", "pain / interference", "Brief Pain Inventory", "Pain interference with general activity last 24 hours (0-10)",
     "How much pain interfered with general activity during the last 24 hours (0 = no interference, 10 = complete interference).",
     "coded", "bpi-interfere-0-10", "", "closeMatch", "http://purl.obolibrary.org/obo/NCIT_C100365",
     "Related pain-interference concept; 24-hour 0-10 scale is from BPI."),
    ("cis_18_noenthousiasm", "fatigue / motivation", "CIS20-R", "I don't feel like doing anything",
     "CIS20-R item: agreement with 'I don't feel like doing anything' on a 1-7 scale.",
     "coded", "cis-1-7", "", "relatedMatch", "http://purl.obolibrary.org/obo/NCIT_C130031",
     "Related motivation concept; this is the CIS20-R item."),
    ("cis_13_diff_focus", "fatigue / concentration", "CIS20-R", "It takes a lot of effort to concentrate on things",
     "CIS20-R item: agreement with difficulty concentrating, 1-7 scale.",
     "coded", "cis-1-7", "", "relatedMatch", "http://purl.obolibrary.org/obo/NCIT_C130026",
     "Related concentration concept; this is the CIS20-R item."),
    ("cis_14_phys_bad", "fatigue / energy", "CIS20-R", "Physically I feel I am in bad form",
     "CIS20-R item: agreement with 'Physically I feel I am in bad form' on a 1-7 scale.",
     "coded", "cis-1-7", "", "relatedMatch", "http://purl.obolibrary.org/obo/NCIT_C130027",
     "Related physical-fatigue concept; not an exact CIS item code."),
    ("employment_status", "demographics / work", "none", "Which situation applies to you most regarding paid work?",
     "Current main employment or income situation.",
     "coded", "employment-10", "", "relatedMatch", "http://loinc.org/67875-5",
     "Employment-status topic only; PCNN options are study-specific."),
    ("income", "demographics / work", "none", "Net monthly household income",
     "Net monthly household income in euro bands, including partner income if the household is shared.",
     "coded", "income-13", "", "relatedMatch", "http://loinc.org/98161-3",
     "Income topic only; euro cut-points are PCNN-specific."),
    ("onbehalf_who", "participation", "none", "What is your relation to the person for whom you provide information?",
     "Relationship of the informant to the study participant when completing on behalf of someone else.",
     "coded", "onbehalf-8", "", "relatedMatch", "", "Local informant-relationship item."),
    ("onbehalf_who_t", "participation", "none", "How are you related?",
     "Free-text description of the relationship when completing on behalf of someone else.",
     "text", "", "", "relatedMatch", "http://purl.obolibrary.org/obo/NCIT_C83393", ""),
    ("howheardstudy", "participation", "none", "How did you hear about the post-COVID research?",
     "How the respondent learned about the PCNN study.",
     "coded", "howheard-7", "", "relatedMatch", "http://snomed.info/id/780816009", ""),
    ("invitation", "participation", "none", "Which research or organization invited you?",
     "Recruitment source that invited the respondent.",
     "coded", "invitation-3", "", "relatedMatch", "http://purl.obolibrary.org/obo/NCIT_C93448", ""),
    ("studycodept", "participation / contact", "none", "Research code received by email or letter",
     "Study linkage code sent to the participant so questionnaire data can be joined to other PCNN data.",
     "text", "", "", "relatedMatch", "", "Local linkage identifier; not a clinical concept."),
    ("contact_GP", "permissions", "none", "Enter your GP contact details",
     "Free-text general practitioner contact details provided by the respondent.",
     "text", "", "", "relatedMatch", "http://purl.obolibrary.org/obo/NCIT_C60776", ""),
    ("hospital_end", "COVID-19", "none", "Date discharged from hospital",
     "Date the respondent was discharged from hospital; estimation is allowed.",
     "date", "", "", "closeMatch", "http://loinc.org/8649-6",
     "Discharge-date concept; PCNN item allows an estimate."),
    ("hosptial", "COVID-19", "none", "Hospital admission due to corona infection before long-term symptoms",
     "Whether the respondent was admitted to hospital for a coronavirus infection before long-term symptoms started.",
     "coded", "yes-no", "", "relatedMatch", "http://purl.obolibrary.org/obo/NCIT_C25179",
     "Column name keeps the original codebook spelling."),
    ("hospital_treat", "COVID-19", "none", "What applied during hospital admission",
     "Whether ICU admission and/or oxygen treatment applied during hospital admission.",
     "coded", "hospital-treat-3", "", "relatedMatch", "http://snomed.info/id/32485007", ""),
    ("Nxinfected", "COVID-19", "none", "Estimated number of coronavirus infections since February 2020",
     "How often the respondent thinks they were infected with SARS-CoV-2 since the start of the pandemic in the Netherlands.",
     "number", "", "", "relatedMatch", "http://snomed.info/id/840539006", ""),
    ("Nxinfected_confirm", "COVID-19", "none", "Number of infections confirmed by a positive test",
     "How many of the reported infections were confirmed with a positive test.",
     "number", "", "", "relatedMatch", "", ""),
    ("pos_test", "COVID-19", "none", "Positive test before long-term coronavirus complaints",
     "Whether the respondent tested positive before long-term coronavirus complaints started.",
     "coded", "yes-no", "", "relatedMatch", "", ""),
    ("pos_test_type", "COVID-19", "none", "Type of coronavirus test for this result",
     "Type of test used for the reported positive coronavirus result.",
     "coded", "pos-test-type-5", "", "relatedMatch", "http://snomed.info/id/246246002", ""),
    ("pos_test_date", "COVID-19", "none", "Date of this coronavirus test",
     "Date of the reported coronavirus test; estimation is allowed.",
     "date", "", "", "relatedMatch", "http://purl.obolibrary.org/obo/NCIT_C82512", ""),
    ("pc_confirmedby", "COVID-19", "none", "Who told you that you had long COVID / post-COVID syndrome?",
     "Source of the long-COVID or post-COVID syndrome attribution.",
     "coded", "pc-confirmedby-6", "", "relatedMatch", "http://snomed.info/id/1119303003", ""),
    ("vaccin", "COVID-19 / vaccination", "none", "Have you been vaccinated against the coronavirus?",
     "Whether the respondent received any SARS-CoV-2 vaccination.",
     "coded", "yes-no-unknown", "", "relatedMatch", "http://loinc.org/97073-1", ""),
    ("vaccin_N", "COVID-19 / vaccination", "none", "Number of coronavirus vaccinations",
     "How many coronavirus vaccinations the respondent has received.",
     "number", "", "", "relatedMatch", "http://loinc.org/97073-1", ""),
    ("vaccin_LTc_Nvacc", "COVID-19 / vaccination", "none", "After how many vaccinations did vaccine-related long-term complaints start?",
     "Number of coronavirus vaccinations received before long-term complaints attributed to vaccination started.",
     "number", "", "", "relatedMatch", "", ""),
    ("vaccin_LTc_date", "COVID-19 / vaccination", "none", "Date of the vaccination linked to post-COVID vaccination syndrome",
     "Date of the vaccination after which post-COVID vaccination syndrome started; estimation allowed.",
     "date", "", "", "relatedMatch", "", ""),
    ("vaccin_LTc_Nvirus", "COVID-19 / vaccination", "none", "Vaccinations received before coronavirus-related long-term complaints",
     "Number of vaccinations received before long-term complaints attributed to the coronavirus started.",
     "number", "", "", "relatedMatch", "", ""),
    ("vaccin_LTc_other", "COVID-19 / vaccination", "none", "Long-term complaints after a non-COVID vaccination",
     "Whether the respondent ever had long-term complaints after a non-COVID vaccination, for example a travel vaccine or flu shot.",
     "coded", "vaccin-ltc-other", "", "relatedMatch", "http://loinc.org/66375-7", ""),
    ("whodiagnosed", "COVID-19 / vaccination", "none", "Who told you that you had post-COVID vaccination syndrome?",
     "Source of the post-COVID vaccination syndrome attribution.",
     "coded", "pc-confirmedby-6", "", "relatedMatch", "", ""),
    ("LTcompl_virus", "long-term complaints / COVID-19", "none", "Current long-term health complaints due to the coronavirus",
     "Whether the respondent currently has long-term health complaints attributed to the coronavirus.",
     "coded", "yes-no-recovered", "", "relatedMatch", "http://snomed.info/id/1119304009", ""),
    ("LTcompl_virus_start", "long-term complaints / COVID-19", "none", "Approximate start date of coronavirus-related long-term complaints",
     "Estimated start date of long-term complaints attributed to the coronavirus.",
     "date", "", "", "relatedMatch", "http://snomed.info/id/298059007", ""),
    ("LTcompl_virus_recover", "long-term complaints / COVID-19", "none", "Approximate recovery date from coronavirus-related long-term complaints",
     "Estimated date of recovery from long-term complaints attributed to the coronavirus.",
     "date", "", "", "relatedMatch", "", ""),
    ("LTcompl_vacc", "long-term complaints / vaccination", "none", "Current long-term health complaints due to a coronavirus vaccination",
     "Whether the respondent currently has long-term health complaints attributed to a coronavirus vaccination.",
     "coded", "yes-no-recovered", "", "relatedMatch", "http://snomed.info/id/293104008", ""),
    ("LTcompl_vacc_recover", "long-term complaints / vaccination", "none", "Approximate recovery date from vaccine-related long-term complaints",
     "Estimated date of recovery from long-term complaints attributed to the coronavirus vaccine.",
     "date", "", "", "relatedMatch", "http://snomed.info/id/293104008", ""),
    ("depression_history", "mental health", "none", "Have you ever suffered from depressive symptoms?",
     "Lifetime history of depressive symptoms, with optional year of last episode.",
     "coded", "depression-history", "", "relatedMatch", "http://snomed.info/id/394924000", ""),
    ("s31_skin_where", "symptoms / POTS", "COMPASS-31", "Which body parts are affected by these colour changes?",
     "COMPASS-31 item: body regions affected by skin colour changes.",
     "coded", "s31-skin-2", "", "relatedMatch", "http://snomed.info/id/364533002", ""),
    ("c31_dry_mouth", "symptoms / POTS", "COMPASS-31", "Does your mouth feel abnormally dry?",
     "COMPASS-31 item asking whether the mouth feels abnormally dry.",
     "coded", "c31-dry-mouth", "", "closeMatch", "http://loinc.org/63981-5",
     "Close to PhenX/LOINC 63981-5 ('frequently dry') but this is the COMPASS-31 wording ('abnormally dry')."),
    ("c31_drrhea_freq_n", "symptoms / POTS", "COMPASS-31", "How many times per month? (diarrhea)",
     "COMPASS-31 count of diarrhea episodes per month.",
     "number", "", "/mo", "relatedMatch", "http://loinc.org/69711-0", ""),
    ("c31_bladder_freq_n", "symptoms / POTS", "COMPASS-31", "How many times per month? (bladder)",
     "COMPASS-31 count of bladder-related episodes per month.",
     "number", "", "/mo", "relatedMatch", "", ""),
    ("c31_eyes_change", "symptoms / POTS", "COMPASS-31", "This most annoying eye complaint is",
     "COMPASS-31 item identifying the most annoying eye complaint.",
     "text", "", "", "relatedMatch", "", ""),
    ("calcc31_eyes_change", "symptoms / POTS", "COMPASS-31", "COMPASS dependency (eyes)",
     "Derived COMPASS-31 eyes-change dependency score calculated by the study pipeline.",
     "number", "", "", "", "", "Derived variable; not a questionnaire item."),
    ("permission", "permissions", "none", "May we contact you for additional scientific research?",
     "Consent to be approached for additional PCNN scientific research.",
     "coded", "permission-2", "", "relatedMatch", "http://purl.obolibrary.org/obo/NCIT_C125453", ""),
    ("permission_pc", "permissions", "none", "Consent form for post-COVID research",
     "Record that the post-COVID research consent form was presented or completed.",
     "text", "", "", "relatedMatch", "http://snomed.info/id/75554001", ""),
    ("persmission_postvacc", "permissions", "none", "Consent form for post-COVID vaccination complaints research",
     "Record that the post-vaccination complaints consent form was presented or completed. Column name keeps the original codebook spelling.",
     "text", "", "", "relatedMatch", "http://snomed.info/id/75554001", ""),
    ("permissions_check", "permissions", "none", "Confirmation that additional-research permission was not given",
     "Check item confirming that the respondent did not give permission to be approached for additional research.",
     "coded", "permissions-check", "", "", "", ""),
    ("travel", "permissions", "none", "Able and willing to travel for additional research",
     "Whether the respondent can travel to take part in additional research.",
     "coded", "travel-3", "", "relatedMatch", "", ""),
    ("contact", "permissions", "none", "May we contact you for a telephone or video appointment?",
     "Consent to be contacted by phone or video for additional research.",
     "coded", "yes-no", "", "relatedMatch", "", ""),
]


def ttl_escape(s):
    return s.replace("\\", "\\\\").replace('"', '\\"')


def write_csv():
    path = ROOT / "variables.csv"
    fields = [
        "column_name", "local_iri", "persistent_iri", "theme", "instrument",
        "prefLabel_en", "definition_en", "datatype", "value_set_id", "unit",
        "mapping_relation", "mapping_uri", "mapping_note",
    ]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for row in VARS:
            col, theme, inst, label, defin, dtype, vsid, unit, rel, uri, note = row
            w.writerow({
                "column_name": col,
                "local_iri": f"var:{col}",
                "persistent_iri": f"{VAR}{col}",
                "theme": theme,
                "instrument": inst,
                "prefLabel_en": label,
                "definition_en": defin,
                "datatype": dtype,
                "value_set_id": vsid,
                "unit": unit,
                "mapping_relation": rel,
                "mapping_uri": uri,
                "mapping_note": note,
            })
    vs_path = ROOT / "valuesets.csv"
    with vs_path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["value_set_id", "code", "label_en", "value_iri"])
        w.writeheader()
        for vsid, items in VALUE_SETS.items():
            for code, lab in items:
                w.writerow({
                    "value_set_id": vsid,
                    "code": code,
                    "label_en": lab,
                    "value_iri": f"{VS}{vsid}/{code}",
                })


def write_ttl():
    lines = [
        "@prefix skos: <http://www.w3.org/2004/02/skos/core#> .",
        "@prefix dct:  <http://purl.org/dc/terms/> .",
        "@prefix owl:  <http://www.w3.org/2002/07/owl#> .",
        "@prefix xsd:  <http://www.w3.org/2001/XMLSchema#> .",
        f"@prefix :     <{NS}> .",
        f"@prefix var:  <{VAR}> .",
        f"@prefix vs:   <{VS}> .",
        "",
        ": a skos:ConceptScheme ;",
        '  dct:title "PCNN variable vocabulary"@en ;',
        '  dct:description "Local persistent identifiers for PCNN study questionnaire and demographic items. Mappings to LOINC, SNOMED CT or NCIT are annotations, not replacements for the PCNN item IRI."@en ;',
        '  dct:creator "PCNN study team" ;',
        '  dct:created "2026-09-08"^^xsd:date ;',
        '  dct:modified "2026-09-08"^^xsd:date ;',
        "  dct:license <https://creativecommons.org/licenses/by/4.0/> ;",
        '  owl:versionInfo "0.1.0" ;',
        '  dct:source "PCNN multilingual codebook; source instruments cited per item." .',
        "",
    ]
    for vsid, items in VALUE_SETS.items():
        lines.append(f"vs:{vsid} a skos:ConceptScheme ;")
        lines.append(f'  dct:title "{ttl_escape(vsid)}"@en .')
        lines.append("")
        for code, lab in items:
            safe = code.replace(".", "_")
            lines.append(f"<{VS}{vsid}/{code}> a skos:Concept ;")
            lines.append(f"  skos:inScheme vs:{vsid} ;")
            lines.append(f'  skos:notation "{ttl_escape(code)}" ;')
            lines.append(f'  skos:prefLabel "{ttl_escape(lab)}"@en .')
            lines.append("")
    for row in VARS:
        col, theme, inst, label, defin, dtype, vsid, unit, rel, uri, note = row
        lines.append(f"var:{col} a skos:Concept ;")
        lines.append("  skos:inScheme : ;")
        lines.append(f'  skos:prefLabel "{ttl_escape(label)}"@en ;')
        lines.append(f'  skos:altLabel "{ttl_escape(col)}" ;')
        lines.append(f'  skos:notation "{ttl_escape(col)}" ;')
        lines.append(f'  skos:definition "{ttl_escape(defin)}"@en ;')
        scope = f"Theme: {theme}. Instrument: {inst}. Datatype: {dtype}."
        if vsid:
            scope += f" Value set: vs:{vsid}."
        if unit:
            scope += f" Unit: {unit}."
        if note:
            scope += " " + note
        lines.append(f'  skos:scopeNote "{ttl_escape(scope)}"@en')
        extra = []
        if inst and inst != "none":
            extra.append(f'  dct:source "{ttl_escape(inst)}"')
        if rel and uri:
            extra.append(f"  skos:{rel} <{uri}>")
        if extra:
            lines[-1] += " ;"
            for i, e in enumerate(extra):
                lines.append(e + (" ." if i == len(extra) - 1 else " ;"))
        else:
            lines[-1] += " ."
        lines.append("")
    text = "\n".join(lines) + "\n"
    (ROOT / "vocabulary.ttl").write_text(text, encoding="utf-8")
    (DOCS / "vocabulary.ttl").write_text(text, encoding="utf-8")


def write_html():
    rows = []
    for row in VARS:
        col, theme, inst, label, defin, dtype, vsid, unit, rel, uri, note = row
        iri = f"{VAR}{col}"
        mapcell = ""
        if rel and uri:
            mapcell = f'{html.escape(rel)} <a href="{html.escape(uri)}">{html.escape(uri)}</a>'
        elif note:
            mapcell = html.escape(note)
        rows.append(f"""<tr id="{html.escape(col)}">
<td><code>{html.escape(col)}</code></td>
<td>{html.escape(label)}</td>
<td>{html.escape(inst)}</td>
<td>{html.escape(dtype)}</td>
<td><a href="{html.escape(iri)}">{html.escape(iri)}</a></td>
<td>{mapcell}</td>
</tr>""")
    page = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>PCNN variable vocabulary</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 2rem; max-width: 1200px; }}
    table {{ border-collapse: collapse; width: 100%; font-size: 0.92rem; }}
    th, td {{ border: 1px solid #ccc; padding: 0.4rem 0.5rem; vertical-align: top; }}
    th {{ background: #f4f4f4; text-align: left; }}
    code {{ font-size: 0.88rem; }}
  </style>
</head>
<body>
  <h1>PCNN variable vocabulary</h1>
  <p>Version 0.1.0. Local test page for PCNN item identifiers.</p>
  <p>Persistent IRI pattern:
     <code>https://w3id.org/pcnn/var/{{column_name}}</code>
     (resolves after the w3id pull request is merged; until then use this page).</p>
  <p>Machine-readable file: <a href="vocabulary.ttl">vocabulary.ttl</a></p>
  <p>Instrument item wording remains copyright of the original instrument authors.
     This page publishes PCNN identifiers, short English labels, definitions and mappings.</p>
  <table>
    <thead>
      <tr>
        <th>Column</th><th>English label</th><th>Instrument</th>
        <th>Datatype</th><th>Persistent IRI</th><th>Mapping</th>
      </tr>
    </thead>
    <tbody>
      {''.join(rows)}
    </tbody>
  </table>
</body>
</html>
"""
    (DOCS / "index.html").write_text(page, encoding="utf-8")


def write_readme():
    (ROOT / "README.md").write_text(
        """# PCNN variable vocabulary

Local and persistent identifiers for PCNN study variables.

- Persistent IRI pattern: `https://w3id.org/pcnn/var/{column_name}`
- Version: 0.1.0
- License for this encoding: [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/)

## What is in this repository

| File | Purpose |
|---|---|
| `variables.csv` | One row per PCNN column: local name, persistent IRI, definition, mapping |
| `valuesets.csv` | Shared answer lists |
| `vocabulary.ttl` | SKOS encoding |
| `docs/index.html` | Human-readable table for local testing and GitHub Pages |
| `docs/vocabulary.ttl` | Copy of the SKOS file for the website folder |

Item wording from DSQ, BPI, CIS20-R and COMPASS-31 remains copyright of the original authors. This repository publishes PCNN identifiers, short English labels, definitions written by the PCNN team, coded value lists needed to interpret PCNN data, and mappings.

## Test locally now

1. Open `docs/index.html` in a browser.
2. Open `variables.csv` in Excel or LibreOffice.
3. Optional: open `vocabulary.ttl` in a text editor.

You do not need GitHub Pages or w3id for this test. The persistent IRIs are already written in the files. They will start resolving on the web after you:

1. Put this folder in a public GitHub repository.
2. Enable GitHub Pages on the `docs/` folder.
3. Open a pull request to [w3id.org](https://github.com/perma-id/w3id.org) for the `pcnn/` path.

Until w3id is approved, keep the same IRIs in your data dictionary. Do not change them later.

## Mapping policy

- Every PCNN column has a PCNN IRI.
- `exactMatch` is used only when question, timeframe, scale and answer list are the same.
- `closeMatch` means the same topic with small differences.
- `relatedMatch` means a related concept only.
- An empty mapping is allowed when no suitable public item exists (common for DSQ-2 items).

Mappings do not replace the PCNN identifier.
""",
        encoding="utf-8",
    )


def write_license_citation():
    (ROOT / "LICENSE").write_text(
        "This PCNN encoding is licensed under Creative Commons Attribution 4.0 International (CC BY 4.0).\n"
        "https://creativecommons.org/licenses/by/4.0/\n",
        encoding="utf-8",
    )
    (ROOT / "CITATION.cff").write_text(
        """cff-version: 1.2.0
title: PCNN variable vocabulary
message: If you use these PCNN item IRIs, please cite this vocabulary.
type: dataset
version: 0.1.0
license: CC-BY-4.0
""",
        encoding="utf-8",
    )


if __name__ == "__main__":
    write_csv()
    write_ttl()
    write_html()
    write_readme()
    write_license_citation()
    print(f"Wrote {len(VARS)} variables and {len(VALUE_SETS)} value sets.")
