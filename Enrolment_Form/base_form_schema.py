BASE_FORM_SCHEMA = {
    "sections": [
        {
            "section_number": "6.1.2",
            "section_title": "Student Personal Details",
            "order": 1,
            "questions": [
                {"key": "legal_name", "label": "Legal name", "type": "text", "required": True, "order": 1},
                {"key": "preferred_name", "label": "Preferred name", "type": "text", "required": True, "order": 2},
                {"key": "date_of_birth", "label": "Date of birth", "type": "date", "required": True, "order": 3},
                {"key": "gender", "label": "Gender", "type": "select", "required": True, "order": 4, "choices": ["Male", "Female", "Other", "Prefer not to say"]},
                {"key": "ethnicity", "label": "Ethnicity (MOE aligned)", "type": "text", "required": True, "order": 5},
                {"key": "iwi_affiliation", "label": "Iwi affiliation", "type": "text", "required": False, "order": 6},
                {"key": "nsn", "label": "NSN (if available)", "type": "text", "required": False, "order": 7},
                {"key": "citizenship_status", "label": "Citizenship / residency status", "type": "text", "required": True, "order": 8}
            ]
        },

        {
            "section_number": "6.1.3",
            "section_title": "Family & Emergency Contacts",
            "order": 2,
            "questions": [
                {"key": "parent1_name", "label": "Parent/Caregiver 1 Name", "type": "text", "required": True, "order": 1},
                {"key": "parent1_relationship", "label": "Relationship to student", "type": "text", "required": True, "order": 2},
                {"key": "parent1_phone", "label": "Phone Number", "type": "text", "required": True, "order": 3},

                {"key": "parent2_name", "label": "Parent/Caregiver 2 Name", "type": "text", "required": False, "order": 4},
                {"key": "parent2_relationship", "label": "Relationship to student", "type": "text", "required": False, "order": 5},
                {"key": "parent2_phone", "label": "Phone Number", "type": "text", "required": False, "order": 6},

                {"key": "emergency_contact_name", "label": "Emergency Contact Name", "type": "text", "required": True, "order": 7},
                {"key": "emergency_contact_phone", "label": "Emergency Contact Phone", "type": "text", "required": True, "order": 8},

                {"key": "custody_restrictions", "label": "Are there custody or legal restrictions?", "type": "boolean", "required": True, "order": 9},
                {"key": "custody_restrictions_details", "label": "Provide details of custody or legal restrictions", "type": "textarea", "required": False, "order": 10, "show_if": {"question_key": "custody_restrictions", "value": True}}
            ]
        },

        {
            "section_number": "6.1.4",
            "section_title": "Address & zoning",
            "order": 3,
            "questions": [
                {
                    "key": "residential_address",
                    "label": "Residential Address",
                    "type": "text",
                    "required": True,
                    "order": 1
                },
                {
                    "key": "postal_address_different",
                    "label": "Is your postal address different?",
                    "type": "boolean",
                    "required": True,
                    "order": 2
                },
                {
                    "key": "postal_address",
                    "label": "Postal Address",
                    "type": "text",
                    "required": False,
                    "order": 3,
                    "show_if": {
                        "question_key": "postal_address_different",
                        "value": True
                    }
                },
                {
                    "key": "proof_of_address",
                    "label": "Upload Proof of Address",
                    "type": "file",
                    "required": True,
                    "order": 4
                }
            ]
        },

        {
            "section_number": "6.1.5",
            "section_title": "Medical & Learning Information",
            "order": 4,
            "questions": [
                {
                    "key": "allergies",
                    "label": "Allergies",
                    "type": "textarea",
                    "required": False,
                    "order": 1
                },
                {
                    "key": "medical_conditions",
                    "label": "Medical Conditions",
                    "type": "textarea",
                    "required": False,
                    "order": 2
                },
                {
                    "key": "medication_requirements",
                    "label": "Medication Requirements",
                    "type": "textarea",
                    "required": False,
                    "order": 3
                },
                {
                    "key": "learning_support_needs",
                    "label": "Learning Support Needs",
                    "type": "textarea",
                    "required": False,
                    "order": 4
                },
                {
                    "key": "previous_school",
                    "label": "Previous School / Early Childhood Education",
                    "type": "text",
                    "required": False,
                    "order": 5
                }
            ]
        }
    ]
}