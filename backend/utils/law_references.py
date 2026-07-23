"""
Legal information and law references for different cyber crime types.
"""
from django.utils.translation import gettext_lazy as _
from .url_encoder import normalize_url

_RAW_CYBER_LAW_REFERENCES = {
    'phishing': {
        'name': _('Phishing'),
        'description': _('Fraudulent attempts to obtain sensitive information by disguising as trustworthy entities'),
        'relevant_laws': [
            {
                'law_name': _('Information Technology Act, 2000'),
                'sections': [_('Section 66'), _('Section 66C'), _('Section 66D')],
                'details': {
                    'section_66': {
                        'title': _('Section 66 - Computer Related Offences'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹5 lakh'),
                        'description': _('Whoever commits an offence of fraud, forgery or cheating by impersonation shall be punishable with imprisonment and fine.')
                    },
                    'section_66c': {
                        'title': _('Section 66C - Identity Theft'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹1 lakh'),
                        'description': _('Whoever fraudulently or dishonestly makes use of electronic signature, password or any other unique identification feature of any other person shall be punishable.')
                    },
                    'section_66d': {
                        'title': _('Section 66D - Phishing'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹1 lakh'),
                        'description': _('Whoever, by means of any electronic record, makes any misrepresentation to induce any person to part with any money, valuable security or property shall be punishable.')
                    }
                }
            },
            {
                'law_name': _('Indian Penal Code (IPC)'),
                'sections': [_('Section 420'), _('Section 406'), _('Section 409')],
                'details': {
                    'section_420': {
                        'title': _('Section 420 - Cheating and Dishonestly Inducing Delivery of Property'),
                        'punishment': _('Imprisonment up to 7 years and fine up to ₹10 lakh'),
                        'description': _('Whoever cheats and by means of such cheating induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, or makes an entry in any book or record.')
                    },
                    'section_406': {
                        'title': _('Section 406 - Punishment for Criminal Breach of Trust'),
                        'punishment': _('Imprisonment up to 7 years and fine up to ₹1 lakh'),
                        'description': _('Whoever, being in any manner entrusted with property, or with any dominion over property, dishonestly misappropriates or converts to his own use that property, or dishonestly uses or causes to be used that property.')
                    }
                }
            }
        ],
        'govt_resources': [
            {
                'name': _('Cyber Crime Helpline - Report Phishing'),
                'url': 'https://cybercrime.gov.in/webform/complaint/',
                'description': _('Report phishing and fraud attempts to Indian Government Cyber Crime Portal')
            },
            {
                'name': _('RBI - Phishing & Fraud Prevention'),
                'url': 'https://www.rbi.org.in/Scripts/BS_ViewContent.aspx?Id=3009',
                'description': _('RBI guidelines on phishing prevention and online security')
            },
            {
                'name': _('CERT-IN - Phishing Alerts'),
                'url': 'https://www.cert-in.org.in/alerts/phishing',
                'description': _('CERT-IN security alerts and advisories on phishing attacks')
            }
        ]
    },
    'identity_theft': {
        'name': _('Identity Theft'),
        'description': _('Stealing personal information to commit fraud or open fake accounts'),
        'relevant_laws': [
            {
                'law_name': _('Information Technology Act, 2000'),
                'sections': [_('Section 66C'), _('Section 66E')],
                'details': {
                    'section_66c': {
                        'title': _('Section 66C - Identity Theft'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹1 lakh'),
                        'description': _('Whoever fraudulently or dishonestly makes use of electronic signature, password or any other unique identification feature of any other person shall be punishable.')
                    },
                    'section_66e': {
                        'title': _('Section 66E - Violation of Privacy'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹2 lakh'),
                        'description': _('Whoever captures, publishes or transmits the image of a private area of any person without his/her consent shall be punishable.')
                    }
                }
            },
            {
                'law_name': _('Indian Penal Code (IPC)'),
                'sections': [_('Section 406'), _('Section 420'), _('Section 468')],
                'details': {
                    'section_406': {
                        'title': _('Section 406 - Criminal Breach of Trust'),
                        'punishment': _('Imprisonment up to 7 years and fine up to ₹1 lakh'),
                        'description': _('Dishonest misappropriation of property or personal information entrusted with a person.')
                    },
                    'section_420': {
                        'title': _('Section 420 - Cheating and Dishonestly Inducing Delivery of Property'),
                        'punishment': _('Imprisonment up to 7 years and fine up to ₹10 lakh'),
                        'description': _('Whoever cheats and by means of such cheating induces the person deceived to deliver any property.')
                    },
                    'section_468': {
                        'title': _('Section 468 - Forgery for Purpose of Cheating'),
                        'punishment': _('Imprisonment up to 7 years and fine up to ₹10 lakh'),
                        'description': _('Whoever commits forgery intending that the forged document shall be used for cheating or as a substitute for any material object.')
                    }
                }
            },
            {
                'law_name': _('Aadhaar Act, 2016'),
                'sections': [_('Section 23')],
                'details': {
                    'section_23': {
                        'title': _('Section 23 - Punishment for Wrongfully Collecting/Using Aadhaar Data'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹10 lakh'),
                        'description': _('Collecting Aadhaar information without consent or using it improperly.')
                    }
                }
            }
        ],
        'govt_resources': [
            {
                'name': _('Cyber Crime Helpline - Identity Theft'),
                'url': 'https://cybercrime.gov.in/webform/complaint/',
                'description': _('Report identity theft and fraud to Indian Government Cyber Crime Portal')
            },
            {
                'name': _('UIDAI - Identity Protection'),
                'url': 'https://www.uidai.gov.in/protecting-your-information',
                'description': _('Aadhaar Authority guidelines on protecting your personal identity and preventing theft')
            },
            {
                'name': _('NCRB - Identity Crime Data'),
                'url': 'https://ncrb.gov.in/cyber-crime',
                'description': _('National Crime Records Bureau statistics on identity-related crimes')
            }
        ]
    },
    'online_fraud': {
        'name': _('Online Fraud'),
        'description': _('Financial fraud, scams, and deceptive practices conducted online'),
        'relevant_laws': [
            {
                'law_name': _('Information Technology Act, 2000'),
                'sections': [_('Section 66'), _('Section 66D')],
                'details': {
                    'section_66': {
                        'title': _('Section 66 - Computer Related Offences'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹5 lakh'),
                        'description': _('Commits an offence of fraud, forgery or cheating by impersonation in cyberspace.')
                    },
                    'section_66d': {
                        'title': _('Section 66D - Punishment for Cheating by Personation by Using Computer Resource'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹1 lakh'),
                        'description': _('Making misrepresentation by means of any electronic record to induce a person to part with money or property.')
                    }
                }
            },
            {
                'law_name': _('Indian Penal Code (IPC)'),
                'sections': [_('Section 420'), _('Section 406'), _('Section 511')],
                'details': {
                    'section_420': {
                        'title': _('Section 420 - Cheating and Dishonestly Inducing Delivery of Property'),
                        'punishment': _('Imprisonment up to 7 years and fine'),
                        'description': _('Cheating by which the victim is induced to deliver any property or valuable security.')
                    },
                    'section_511': {
                        'title': _('Section 511 - Punishment for Attempting to Commit Offences'),
                        'punishment': _('Half the punishment for the actual offence'),
                        'description': _('Attempted commission of offences, including attempted fraud.')
                    }
                }
            }
        ],
        'govt_resources': [
            {
                'name': _('Cyber Crime Helpline - Online Fraud'),
                'url': 'https://cybercrime.gov.in/webform/complaint/',
                'description': _('Report online fraud and financial scams to official portal')
            },
            {
                'name': _('RBI - Online Fraud Prevention'),
                'url': 'https://www.rbi.org.in/Scripts/BS_ViewContent.aspx?Id=3010',
                'description': _('RBI guidelines on preventing online financial fraud and safe banking')
            },
            {
                'name': _('SEBI - Investor Protection'),
                'url': 'https://www.sebi.gov.in/sebiweb/home/homepagesimp1.jsp?sid=investor%20grievance',
                'description': _('SEBI guidelines on securities fraud and investor complaint resolution')
            }
        ]
    },
    'hacking': {
        'name': _('Hacking'),
        'description': _('Unauthorized access to computer systems and networks'),
        'relevant_laws': [
            {
                'law_name': _('Information Technology Act, 2000'),
                'sections': [_('Section 43'), _('Section 66')],
                'details': {
                    'section_43': {
                        'title': _('Section 43 - Penalty for Damage to Computer, Computer System, etc.'),
                        'punishment': _('Compensation up to ₹1 crore'),
                        'description': _('Civil liability for unauthorized access, data theft, or system damage.')
                    },
                    'section_66': {
                        'title': _('Section 66 - Computer Related Offences'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹5 lakh'),
                        'description': _('Criminal offense for hacking, unauthorized access, and system manipulation.')
                    }
                }
            },
            {
                'law_name': _('Indian Penal Code (IPC)'),
                'sections': [_('Section 420'), _('Section 379'), _('Section 405')],
                'details': {
                    'section_420': {
                        'title': _('Section 420 - Cheating'),
                        'punishment': _('Imprisonment up to 7 years and fine'),
                        'description': _('If hacking is done to cheat or defraud a person.')
                    },
                    'section_379': {
                        'title': _('Section 379 - Punishment for Theft'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹2,000'),
                        'description': _('If data or information is stolen through hacking.')
                    }
                }
            }
        ],
        'govt_resources': [
            {
                'name': _('Cyber Crime Helpline - Hacking'),
                'url': 'https://cybercrime.gov.in/webform/complaint/',
                'description': _('Report unauthorized access and hacking incidents')
            },
            {
                'name': _('CERT-IN - Hacking Advisories'),
                'url': 'https://www.cert-in.org.in/alerts/vulnerabilities',
                'description': _('CERT-IN security alerts on unauthorized access and exploits')
            },
            {
                'name': _('MeitY - Cybersecurity Guidelines'),
                'url': 'https://www.meity.gov.in/divisions/cybersecurity',
                'description': _('Government cybersecurity guidelines and best practices')
            }
        ]
    },
    'ransomware': {
        'name': _('Ransomware'),
        'description': _('Malware that encrypts data and demands ransom for decryption'),
        'relevant_laws': [
            {
                'law_name': _('Information Technology Act, 2000'),
                'sections': [_('Section 66'), _('Section 66B')],
                'details': {
                    'section_66': {
                        'title': _('Section 66 - Computer Related Offences'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹5 lakh'),
                        'description': _('Unauthorized alteration, damage or denial of access to computer systems.')
                    },
                    'section_66b': {
                        'title': _('Section 66B - Punishment for Stealing Computer Material or Data'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹2 lakh'),
                        'description': _('Stealing or acquiring computer source code or confidential information.')
                    }
                }
            },
            {
                'law_name': _('Indian Penal Code (IPC)'),
                'sections': [_('Section 383'), _('Section 384'), _('Section 420')],
                'details': {
                    'section_383': {
                        'title': _('Section 383 - Extortion'),
                        'punishment': _('Imprisonment up to 6 months and fine up to ₹500'),
                        'description': _('Putting a person in fear of injury to extort property or services.')
                    },
                    'section_384': {
                        'title': _('Section 384 - Punishment for Extortion'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹2,000'),
                        'description': _('Using threats or coercion to extort money or property.')
                    }
                }
            }
        ],
        'govt_resources': [
            {
                'name': _('Cyber Crime Helpline - Ransomware'),
                'url': 'https://cybercrime.gov.in/webform/complaint/',
                'description': _('Report ransomware attacks and extortion incidents')
            },
            {
                'name': _('CERT-IN - Ransomware Alerts'),
                'url': 'https://www.cert-in.org.in/alerts/ransomware',
                'description': _('CERT-IN warnings and advisories on active ransomware threats')
            },
            {
                'name': _('MeitY - Incident Response'),
                'url': 'https://www.meity.gov.in/divisions/incident-response',
                'description': _('Government incident response guidelines for ransomware attacks')
            }
        ]
    },
    'data_breach': {
        'name': _('Data Breach'),
        'description': _('Unauthorized access or exposure of sensitive personal data'),
        'relevant_laws': [
            {
                'law_name': _('Information Technology Act, 2000'),
                'sections': [_('Section 43A'), _('Section 66'), _('Section 72')],
                'details': {
                    'section_43a': {
                        'title': _('Section 43A - Failure to Protect Personal Data'),
                        'punishment': _('Compensation up to ₹50 crore'),
                        'description': _('Compensation for failure to protect personal data and privacy.')
                    },
                    'section_66': {
                        'title': _('Section 66 - Computer Related Offences'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹5 lakh'),
                        'description': _('Unauthorized disclosure of data or system interference.')
                    },
                    'section_72': {
                        'title': _('Section 72 - Breach of Confidentiality and Privacy'),
                        'punishment': _('Imprisonment up to 2 years and fine up to ₹1 lakh'),
                        'description': _('Communicating, retaining or securing any electronic record without consent.')
                    }
                }
            },
            {
                'law_name': _('Digital Personal Data Protection Act, 2023'),
                'sections': [_('Section 6'), _('Section 8')],
                'details': {
                    'section_6': {
                        'title': _('Section 6 - Rights of Data Principal'),
                        'punishment': _('Administrative penalties'),
                        'description': _('Right to privacy and access to personal data processing information.')
                    },
                    'section_8': {
                        'title': _('Section 8 - Consent Requirements'),
                        'punishment': _('Penalties for non-compliance'),
                        'description': _('Processing of personal data must be done with explicit consent.')
                    }
                }
            }
        ],
        'govt_resources': [
            {
                'name': _('Cyber Crime Helpline - Data Breach'),
                'url': 'https://cybercrime.gov.in/webform/complaint/',
                'description': _('Report data breaches and unauthorized data disclosure')
            },
            {
                'name': _('CERT-IN - Data Security Advisories'),
                'url': 'https://www.cert-in.org.in/alerts/data-security',
                'description': _('CERT-IN advisories on data breaches and security incidents')
            },
            {
                'name': _('MeitY - Data Protection Framework'),
                'url': 'https://www.meity.gov.in/divisions/data-protection',
                'description': _('Government data protection policies and regulations')
            }
        ]
    },
    'cyberbullying': {
        'name': _('Cyberbullying'),
        'description': _('Harassment, threats, or abusive behavior through digital channels'),
        'relevant_laws': [
            {
                'law_name': _('Information Technology Act, 2000'),
                'sections': [_('Section 66A'), _('Section 67'), _('Section 67A')],
                'details': {
                    'section_66a': {
                        'title': _('Section 66A - Sending Offensive Messages Through Communication Service'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹5 lakh'),
                        'description': _('Sending any information which is grossly offensive or menacing in nature.')
                    },
                    'section_67': {
                        'title': _('Section 67 - Publishing Obscene Material in Electronic Form'),
                        'punishment': _('Imprisonment up to 5 years and fine up to ₹10 lakh'),
                        'description': _('Publishing or transmitting obscene material online.')
                    },
                    'section_67a': {
                        'title': _('Section 67A - Publishing Sexually Explicit Material'),
                        'punishment': _('Imprisonment up to 7 years and fine up to ₹10 lakh'),
                        'description': _('Publishing sexually explicit material in electronic form.')
                    }
                }
            },
            {
                'law_name': _('Indian Penal Code (IPC)'),
                'sections': [_('Section 294'), _('Section 354'), _('Section 509')],
                'details': {
                    'section_294': {
                        'title': _('Section 294 - Obscene Acts and Songs'),
                        'punishment': _('Imprisonment up to 3 months and fine up to ₹250'),
                        'description': _('Obscene acts or words intended to be seen or heard by the public.')
                    },
                    'section_354': {
                        'title': _('Section 354 - Assault or Criminal Force with Intent to Outrage Modesty'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹2,000'),
                        'description': _('Sexual harassment including cyberbullying of a sexual nature.')
                    },
                    'section_509': {
                        'title': _('Section 509 - Word, Gesture or Act Intended to Insult Modesty'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹2,000'),
                        'description': _('Insulting words or behavior intended to insult a woman\'s modesty.')
                    }
                }
            },
            {
                'law_name': _('Bharatiya Nyaya Sanhita (BNS), 2023'),
                'sections': [_('Section 351'), _('Section 352')],
                'details': {
                    'section_351': {
                        'title': _('Section 351 - Criminal Intimidation'),
                        'punishment': _('Imprisonment up to 2 years and fine'),
                        'description': _('Threatening or intimidating through any communication channel.')
                    }
                }
            }
        ],
        'govt_resources': [
            {
                'name': _('Cyber Crime Helpline - Cyberbullying'),
                'url': 'https://cybercrime.gov.in/webform/complaint/',
                'description': _('Report cyberbullying and harassment incidents')
            },
            {
                'name': _('NCW - Online Harassment Resources'),
                'url': 'https://ncw.gov.in/resources/articles/cyber-harassment',
                'description': _('National Commission for Women guidelines on cyber harassment of women')
            },
            {
                'name': _('CHILDLINE - Child Cyberbullying'),
                'url': 'https://childlineindia.org.in',
                'description': _('Report cyberbullying of children and minors')
            }
        ]
    },
    'malware': {
        'name': _('Malware Detection & Distribution'),
        'description': _('Creating, distributing, or executing malicious software'),
        'relevant_laws': [
            {
                'law_name': _('Information Technology Act, 2000'),
                'sections': [_('Section 66'), _('Section 66B'), _('Section 66C')],
                'details': {
                    'section_66': {
                        'title': _('Section 66 - Computer Related Offences'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹5 lakh'),
                        'description': _('Unauthorized modification, damage, denial of access, or collection of data.')
                    },
                    'section_66b': {
                        'title': _('Section 66B - Stealing Computer Material or Confidential Information'),
                        'punishment': _('Imprisonment up to 3 years and fine up to ₹2 lakh'),
                        'description': _('Stealing or acquiring computer source code or data through malware.')
                    }
                }
            }
        ],
        'govt_resources': [
            {
                'name': _('Cyber Crime Helpline - Malware Report'),
                'url': 'https://cybercrime.gov.in/webform/complaint/',
                'description': _('Report malware infections and suspicious software')
            },
            {
                'name': _('CERT-IN - Malware Alerts'),
                'url': 'https://www.cert-in.org.in/alerts/malware',
                'description': _('CERT-IN analysis and alerts on malicious software threats')
            },
            {
                'name': _('MeitY - Malware Resources'),
                'url': 'https://www.meity.gov.in/divisions/malware-response',
                'description': _('Government resources for malware detection and removal')
            }
        ]
    },
    'other': {
        'name': _('Other Cyber Crimes'),
        'description': _('Other types of cybercrime not listed above'),
        'relevant_laws': [
            {
                'law_name': _('Information Technology Act, 2000'),
                'sections': [_('Section 43'), _('Section 66')],
                'details': {
                    'section_43': {
                        'title': _('Section 43 - Penalty for Damage to Computer'),
                        'punishment': _('Compensation up to ₹1 crore'),
                        'description': _('Civil and criminal penalties for computer-related damages.')
                    }
                }
            },
            {
                'law_name': _('Indian Penal Code (IPC)'),
                'sections': [_('Multiple sections depending on nature of crime')],
                'details': {}
            }
        ],
        'govt_resources': [
            {
                'name': _('Cyber Crime Helpline - General Report'),
                'url': 'https://cybercrime.gov.in/webform/complaint/',
                'description': _('Report all types of cyber crimes to official portal')
            },
            {
                'name': _('CERT-IN - Security Advisories'),
                'url': 'https://www.cert-in.org.in/alerts',
                'description': _('CERT-IN general security advisories and threat alerts')
            },
            {
                'name': _('MeitY - Cybersecurity Resources'),
                'url': 'https://www.meity.gov.in/divisions/cybersecurity',
                'description': _('Ministry of Electronics and Information Technology resources')
            }
        ]
    }
}


def _encode_urls_in_dict(data):
    """
    Recursively encode all URLs in a dictionary using normalize_url.
    This ensures all special characters are properly percent-encoded.
    """
    if isinstance(data, dict):
        return {key: _encode_urls_in_dict(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [_encode_urls_in_dict(item) for item in data]
    elif isinstance(data, str) and data.startswith('http'):
        # This is a URL - normalize it
        return normalize_url(data)
    else:
        return data


# Process all URLs in the dictionary to ensure proper encoding
CYBER_LAW_REFERENCES = _encode_urls_in_dict(_RAW_CYBER_LAW_REFERENCES)


def get_law_reference(category):
    """
    Get law reference for a complaint category.
    
    Args:
        category (str): The complaint category
        
    Returns:
        dict: The law reference with properly encoded URLs
    """
    return CYBER_LAW_REFERENCES.get(category, CYBER_LAW_REFERENCES['other'])
