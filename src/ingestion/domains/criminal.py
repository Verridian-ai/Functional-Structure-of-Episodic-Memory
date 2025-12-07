"""
Criminal Law Domain Classification
Australian Legal Corpus Classification System

Comprehensive taxonomy for criminal law matters including:
- State-specific criminal codes and legislation
- Offence categories (homicide, sexual, property, drugs, violence, traffic)
- Sentencing terminology and principles
- Criminal defences and mental state
- Procedural and appellate matters

Total keywords: 500+
"""

# =============================================================================
# STATE-SPECIFIC CRIMINAL CODES AND LEGISLATION
# =============================================================================

CRIMINAL_LEGISLATION = {
    # Commonwealth
    'CTH': [
        'Criminal Code Act 1995 (Cth)',
        'Commonwealth Criminal Code',
        'Crimes Act 1914 (Cth)',
        'Proceeds of Crime Act 2002 (Cth)',
        'Crimes (Sentencing Procedure) Act (Cth)',
        'Crimes (Foreign Incursions and Recruitment) Act 1978',
        'Crimes (Aviation) Act 1991',
        'Crimes (Biological Weapons) Act 1976',
        'Crimes (Child Sex Tourism) Amendment Act 1994',
        'Crimes (Hostages) Act 1989',
        'Crimes (Internationally Protected Persons) Act 1976',
        'Crimes (Ships and Fixed Platforms) Act 1992',
        'Crimes (Superannuation Benefits) Act 1989',
        'Crimes (Torture) Act 1988',
        'Crimes (Traffic in Narcotic Drugs and Psychotropic Substances) Act 1990',
        'Criminal Code Amendment (Theft, Fraud, Bribery and Related Offences) Act 2000',
        'Criminal Code Amendment (Terrorist Organisations) Act 2002',
        'Telecommunications (Interception and Access) Act 1979',
        'Surveillance Devices Act 2004',
        'Law Enforcement (Controlled Operations) Act 1997',
    ],

    # New South Wales
    'NSW': [
        'Crimes Act 1900 (NSW)',
        'Crimes (Sentencing Procedure) Act 1999 (NSW)',
        'Criminal Procedure Act 1986 (NSW)',
        'Criminal Appeal Act 1912 (NSW)',
        'Bail Act 2013 (NSW)',
        'Crimes (Forensic Procedures) Act 2000 (NSW)',
        'Crimes (Administration of Sentences) Act 1999 (NSW)',
        'Crimes (Domestic and Personal Violence) Act 2007 (NSW)',
        'Crimes (High Risk Offenders) Act 2006 (NSW)',
        'Child Protection (Offenders Registration) Act 2000 (NSW)',
        'Drug Misuse and Trafficking Act 1985 (NSW)',
        'Confiscation of Proceeds of Crime Act 1989 (NSW)',
        'Law Enforcement (Powers and Responsibilities) Act 2002 (NSW)',
        'Evidence Act 1995 (NSW)',
        'Young Offenders Act 1997 (NSW)',
        'Mental Health (Forensic Provisions) Act 1990 (NSW)',
        'Crimes (Sentencing Legislation) Amendment (Intensive Correction Orders) Act 2010',
        'Crimes Amendment (Sexual Offences) Act 2003',
        'Crimes Amendment (Grievous Bodily Harm) Act 2005',
    ],

    # Victoria
    'VIC': [
        'Crimes Act 1958 (Vic)',
        'Sentencing Act 1991 (Vic)',
        'Criminal Procedure Act 2009 (Vic)',
        'Bail Act 1977 (Vic)',
        'Crimes (Mental Impairment and Unfitness to be Tried) Act 1997 (Vic)',
        'Confiscation Act 1997 (Vic)',
        'Serious Sex Offenders (Detention and Supervision) Act 2009 (Vic)',
        'Sex Offenders Registration Act 2004 (Vic)',
        'Crimes Amendment (Gross Violence Offences) Act 2013 (Vic)',
        'Drugs, Poisons and Controlled Substances Act 1981 (Vic)',
        'Family Violence Protection Act 2008 (Vic)',
        'Jury Directions Act 2015 (Vic)',
        'Evidence Act 2008 (Vic)',
        'Children, Youth and Families Act 2005 (Vic)',
        'Corrections Act 1986 (Vic)',
        'Charter of Human Rights and Responsibilities Act 2006 (Vic)',
        'Summary Offences Act 1966 (Vic)',
        'Crimes (Assumed Identities) Act 2004 (Vic)',
        'Crimes (Controlled Operations) Act 2004 (Vic)',
    ],

    # Queensland
    'QLD': [
        'Criminal Code Act 1899 (Qld)',
        'Penalties and Sentences Act 1992 (Qld)',
        'Criminal Code 1899 (Qld)',
        'Youth Justice Act 1992 (Qld)',
        'Bail Act 1980 (Qld)',
        'Criminal Proceeds Confiscation Act 2002 (Qld)',
        'Dangerous Prisoners (Sexual Offenders) Act 2003 (Qld)',
        'Evidence Act 1977 (Qld)',
        'Criminal Law Amendment Act 1945 (Qld)',
        'Drugs Misuse Act 1986 (Qld)',
        'Domestic and Family Violence Protection Act 2012 (Qld)',
        'Child Protection (Offender Reporting and Offender Prohibition Order) Act 2004 (Qld)',
        'Police Powers and Responsibilities Act 2000 (Qld)',
        'Mental Health Act 2016 (Qld)',
        'Criminal Organisation Act 2009 (Qld)',
        'Serious and Organised Crime Legislation Amendment Act 2016 (Qld)',
        'Crime and Corruption Act 2001 (Qld)',
        'Justices Act 1886 (Qld)',
    ],

    # Western Australia
    'WA': [
        'Criminal Code Act Compilation Act 1913 (WA)',
        'Criminal Code 1913 (WA)',
        'Sentencing Act 1995 (WA)',
        'Criminal Procedure Act 2004 (WA)',
        'Bail Act 1982 (WA)',
        'Criminal Appeals Act 2004 (WA)',
        'Criminal Investigation Act 2006 (WA)',
        'Dangerous Sexual Offenders Act 2006 (WA)',
        'Community Protection (Offender Reporting) Act 2004 (WA)',
        'Criminal Property Confiscation Act 2000 (WA)',
        'Misuse of Drugs Act 1981 (WA)',
        'Restraining Orders Act 1997 (WA)',
        'Young Offenders Act 1994 (WA)',
        'Evidence Act 1906 (WA)',
        'Criminal Law (Mentally Impaired Accused) Act 1996 (WA)',
        'Criminal Organisations Control Act 2012 (WA)',
        'Crimes (Confiscation of Profits) Act 1988 (WA)',
    ],

    # South Australia
    'SA': [
        'Criminal Law Consolidation Act 1935 (SA)',
        'Sentencing Act 2017 (SA)',
        'Criminal Procedure Act 1921 (SA)',
        'Summary Procedure Act 1921 (SA)',
        'Bail Act 1985 (SA)',
        'Criminal Assets Confiscation Act 2005 (SA)',
        'Controlled Substances Act 1984 (SA)',
        'Evidence Act 1929 (SA)',
        'Young Offenders Act 1993 (SA)',
        'Child Sex Offenders Registration Act 2006 (SA)',
        'Intervention Orders (Prevention of Abuse) Act 2009 (SA)',
        'Summary Offences Act 1953 (SA)',
        'Criminal Investigation (Covert Operations) Act 2009 (SA)',
        'Criminal Law (High Risk Offenders) Act 2015 (SA)',
        'Mental Health Act 2009 (SA)',
        'Serious and Organised Crime (Control) Act 2008 (SA)',
    ],

    # Tasmania
    'TAS': [
        'Criminal Code Act 1924 (Tas)',
        'Criminal Code 1924 (Tas)',
        'Sentencing Act 1997 (Tas)',
        'Criminal Procedure (Reform and Modernisation) Act 2002 (Tas)',
        'Bail Act 1994 (Tas)',
        'Crime and Punishment (Amendment) Act 1992 (Tas)',
        'Misuse of Drugs Act 2001 (Tas)',
        'Evidence Act 2001 (Tas)',
        'Youth Justice Act 1997 (Tas)',
        'Community Protection (Offender Reporting) Act 2005 (Tas)',
        'Family Violence Act 2004 (Tas)',
        'Justices Act 1959 (Tas)',
        'Mental Health Act 2013 (Tas)',
        'Crime (Confiscation of Profits) Act 1993 (Tas)',
    ],

    # Australian Capital Territory
    'ACT': [
        'Criminal Code 2002 (ACT)',
        'Crimes Act 1900 (ACT)',
        'Crimes (Sentence Administration) Act 2005 (ACT)',
        'Crimes (Sentencing) Act 2005 (ACT)',
        'Criminal Procedure Act 1986 (ACT)',
        'Bail Act 1992 (ACT)',
        'Confiscation of Criminal Assets Act 2003 (ACT)',
        'Drugs of Dependence Act 1989 (ACT)',
        'Evidence Act 2011 (ACT)',
        'Children and Young People Act 2008 (ACT)',
        'Crimes (Child Sex Offenders) Act 2005 (ACT)',
        'Family Violence Act 2016 (ACT)',
        'Mental Health Act 2015 (ACT)',
        'Crimes (Restorative Justice) Act 2004 (ACT)',
    ],

    # Northern Territory
    'NT': [
        'Criminal Code Act 1983 (NT)',
        'Criminal Code 1983 (NT)',
        'Sentencing Act 1995 (NT)',
        'Criminal Procedure Act 1986 (NT)',
        'Bail Act 1982 (NT)',
        'Youth Justice Act 2005 (NT)',
        'Misuse of Drugs Act 1990 (NT)',
        'Evidence (National Uniform Legislation) Act 2011 (NT)',
        'Criminal Property Forfeiture Act 2002 (NT)',
        'Domestic and Family Violence Act 2007 (NT)',
        'Community Welfare Act 1983 (NT)',
        'Justices Act 1928 (NT)',
        'Mental Health and Related Services Act 1998 (NT)',
    ],
}

# =============================================================================
# OFFENCE CATEGORIES - HOMICIDE
# =============================================================================

CRIM_HOMICIDE = [
    # General homicide terms
    'homicide',
    'unlawful killing',
    'causing death',
    'death occasioned by',
    'unlawful homicide',
    'culpable homicide',

    # Murder
    'murder',
    'first degree murder',
    'capital murder',
    'felony murder',
    'constructive murder',
    'intent to kill',
    'intent to cause grievous bodily harm',
    'malice aforethought',
    'murder in the course of',
    'murder by omission',
    'murder of police officer',
    'murder of correctional officer',
    'aggravated murder',

    # Manslaughter
    'manslaughter',
    'voluntary manslaughter',
    'involuntary manslaughter',
    'unlawful and dangerous act manslaughter',
    'criminal negligence manslaughter',
    'gross negligence manslaughter',
    'manslaughter by unlawful and dangerous act',
    'provoked manslaughter',
    'excessive self-defence',
    'diminished responsibility',
    'substantial impairment',
    'abnormality of mind',

    # Specific manslaughter types
    'manslaughter by criminal negligence',
    'manslaughter by omission',
    'corporate manslaughter',
    'industrial manslaughter',
    'vehicular manslaughter',
    'drug supply manslaughter',
    'one punch manslaughter',
    'coward punch',

    # Infanticide and related
    'infanticide',
    'child homicide',
    'neonaticide',
    'filicide',
    'disturbed balance of mind',
    'effect of giving birth',

    # Specific offences
    'causing death by dangerous driving',
    'dangerous driving causing death',
    'culpable driving causing death',
    'negligent driving occasioning death',
    'dangerous operation of vehicle causing death',
    'aggravated dangerous driving causing death',

    # Defensive homicide (historical - Victoria)
    'defensive homicide',
    'excessive force in self-defence',

    # Attempted homicide
    'attempted murder',
    'attempted manslaughter',
    'conspiracy to murder',
    'solicitation to murder',
    'counselling murder',
    'procuring murder',

    # Elements and principles
    'year and a day rule',
    'causation in homicide',
    'substantial and operating cause',
    'novus actus interveniens',
    'break in chain of causation',
    'medical treatment intervening',
    'victim pre-existing condition',
    'thin skull rule',
    'take victim as you find them',
    'acceleration of death',
    'contribution to death',
]

# =============================================================================
# OFFENCE CATEGORIES - SEXUAL OFFENCES
# =============================================================================

CRIM_SEXUAL = [
    # General sexual offences
    'sexual offence',
    'sexual assault',
    'rape',
    'sexual intercourse without consent',
    'sexual penetration without consent',
    'aggravated sexual assault',
    'sexual assault in company',

    # Consent issues
    'absence of consent',
    'lack of consent',
    'consent negated by',
    'reasonable belief in consent',
    'honest and reasonable belief',
    'communicative consent',
    'affirmative consent',
    'consent and intoxication',
    'consent and unconsciousness',
    'consent under duress',
    'consent by deception',
    'mistaken identity consent',

    # Child sexual offences
    'child sexual abuse',
    'child sexual assault',
    'sexual intercourse with child',
    'carnal knowledge',
    'persistent sexual abuse of a child',
    'maintaining sexual relationship with child',
    'aggravated child sexual offence',
    'child under 10',
    'child under 12',
    'child under 14',
    'child under 16',
    'position of trust',
    'position of authority',
    'special care relationship',
    'teacher-student relationship',
    'care worker offence',

    # Indecent offences
    'indecent assault',
    'act of indecency',
    'indecent act',
    'aggravated indecent assault',
    'indecent assault of child',
    'production of indecent material',

    # Child exploitation material
    'child abuse material',
    'child pornography',
    'child exploitation material',
    'possession of child abuse material',
    'production of child abuse material',
    'dissemination of child abuse material',
    'accessing child abuse material',
    'using carriage service for child abuse material',

    # Grooming and related
    'grooming',
    'procuring child',
    'online grooming',
    'using carriage service to groom',
    'preparatory offence',
    'meeting child following grooming',

    # Historical offences
    'historical sexual offence',
    'historical child sexual abuse',
    'delayed complaint',
    'delay in reporting',
    'uncharged acts',
    'relationship evidence',
    'tendency evidence',
    'coincidence evidence',

    # Incest and familial offences
    'incest',
    'sexual relationship with family member',
    'incestuous relationship',
    'lineal descendant',
    'step-relationship',

    # Other sexual offences
    'sexual servitude',
    'sexual slavery',
    'forced marriage',
    'trafficking for sexual exploitation',
    'bestiality',
    'necrophilia',
    'voyeurism',
    'upskirting',
    'image-based abuse',
    'revenge porn',
    'non-consensual sharing of intimate images',
    'sexual exposure',
    'indecent exposure',
    'outraging public decency',

    # Aggravating factors
    'in company',
    'with wounding',
    'inflicting actual bodily harm',
    'inflicting grievous bodily harm',
    'under authority',
    'child victim',
    'vulnerable victim',
    'victim with cognitive impairment',
    'victim with disability',

    # Evidentiary matters
    'Longman warning',
    'Crofts direction',
    'Kilby direction',
    'jury directions sexual offence',
    'good character sexual offence',
    'delay and forensic disadvantage',
    'Robinson direction',
]

# =============================================================================
# OFFENCE CATEGORIES - PROPERTY OFFENCES
# =============================================================================

CRIM_PROPERTY = [
    # Theft and larceny
    'theft',
    'larceny',
    'steal',
    'stealing',
    'dishonestly appropriating',
    'taking without consent',
    'intent to permanently deprive',
    'asportation',
    'petit larceny',
    'grand larceny',
    'aggravated larceny',
    'larceny by servant',
    'larceny by bailiff',
    'shoplifting',
    'retail theft',

    # Robbery
    'robbery',
    'armed robbery',
    'robbery in company',
    'aggravated robbery',
    'robbery with violence',
    'robbery with wounding',
    'robbery whilst armed',
    'robbery with offensive weapon',
    'robbery with dangerous weapon',
    'assault with intent to rob',
    'demanding property with menaces',
    'extortion',
    'blackmail',

    # Burglary and breaking offences
    'burglary',
    'breaking and entering',
    'break enter and steal',
    'break and enter dwelling',
    'break and enter non-dwelling',
    'aggravated break and enter',
    'home invasion',
    'enter with intent',
    'trespass with intent',
    'breaking out of building',
    'being armed with intent',
    'possession of housebreaking implements',
    'going equipped for stealing',

    # Fraud and deception
    'fraud',
    'obtaining property by deception',
    'obtaining financial advantage by deception',
    'dishonestly obtaining',
    'false pretences',
    'fraudulent misappropriation',
    'embezzlement',
    'criminal breach of trust',
    'false accounting',
    'making false document',
    'using false document',
    'identity fraud',
    'identity theft',
    'social security fraud',
    'tax fraud',
    'medicare fraud',
    'insurance fraud',
    'investment fraud',
    'Ponzi scheme',
    'pyramid scheme',
    'boiler room fraud',
    'advance fee fraud',
    'romance scam',
    'business email compromise',

    # Computer and technology crimes
    'computer fraud',
    'unauthorised access to computer',
    'unauthorised modification of data',
    'impairing electronic communication',
    'denial of service',
    'hacking',
    'phishing',
    'ransomware',
    'cryptojacking',
    'cyber fraud',

    # Receiving and handling stolen goods
    'receiving stolen property',
    'goods in custody',
    'handling stolen goods',
    'dishonestly receiving',
    'disposing of stolen property',
    'knowing or believing stolen',
    'recent possession',
    'unexplained possession',
    'receiving proceeds of crime',

    # Criminal damage
    'malicious damage',
    'criminal damage',
    'destroying property',
    'damaging property',
    'arson',
    'aggravated arson',
    'setting fire to property',
    'wilful damage',
    'vandalism',
    'graffiti',
    'defacing property',
    'destroying evidence',

    # Dishonesty offences
    'dishonesty',
    'dishonest intention',
    'claim of right',
    'honest belief',
    'colour of right',

    # White collar crime
    'corporate fraud',
    'securities fraud',
    'insider trading',
    'market manipulation',
    'false trading',
    'misleading or deceptive conduct',
    'director duties breach',
    'insolvent trading',
    'phoenix activity',
    'cartel conduct',
    'bribery',
    'corruption',
    'secret commissions',
    'money laundering',
    'structuring transactions',
    'smurfing',

    # Forgery and counterfeiting
    'forgery',
    'uttering forged document',
    'making false instrument',
    'counterfeiting',
    'counterfeiting currency',
    'possession of equipment for counterfeiting',
]

# =============================================================================
# OFFENCE CATEGORIES - DRUGS
# =============================================================================

CRIM_DRUGS = [
    # General drug terms
    'prohibited drug',
    'controlled substance',
    'dangerous drug',
    'drug of dependence',
    'narcotic drug',
    'psychotropic substance',
    'border controlled drug',
    'border controlled plant',

    # Drug supply and trafficking
    'supply prohibited drug',
    'drug supply',
    'deemed supply',
    'supply by possession',
    'ongoing supply',
    'commercial supply',
    'large commercial supply',
    'drug trafficking',
    'commercial trafficking',
    'trafficking in controlled drug',
    'trafficking drugs of dependence',
    'supplying indictable quantity',
    'supplying commercial quantity',
    'supplying trafficable quantity',
    'supplying marketable quantity',

    # Drug importation
    'import prohibited drug',
    'import border controlled drug',
    'import commercial quantity',
    'import marketable quantity',
    'importation of drugs',
    'smuggling drugs',
    'conspiracy to import',

    # Drug possession
    'possession of prohibited drug',
    'possession of controlled substance',
    'possession for personal use',
    'possession with intent to supply',
    'joint possession',
    'constructive possession',
    'deemed possession',
    'exclusive possession',
    'custody of drugs',

    # Drug manufacture and cultivation
    'manufacture prohibited drug',
    'manufacturing drugs',
    'cultivate prohibited plant',
    'cultivation of cannabis',
    'cultivating narcotic plants',
    'large commercial cultivation',
    'commercial cultivation',
    'enhanced indoor cultivation',
    'hydroponic cultivation',
    'cannabis crop',
    'opium poppy cultivation',

    # Quantities
    'trafficable quantity',
    'indictable quantity',
    'commercial quantity',
    'large commercial quantity',
    'marketable quantity',
    'small quantity',
    'prescribed quantity',
    'deemed commercial quantity',

    # Specific drugs
    'cannabis',
    'marijuana',
    'marihuana',
    'hashish',
    'cannabis resin',
    'cannabis oil',
    'tetrahydrocannabinol',
    'THC',
    'heroin',
    'cocaine',
    'methamphetamine',
    'methylamphetamine',
    'amphetamine',
    'ice',
    'crystal meth',
    'MDMA',
    'ecstasy',
    'GHB',
    'ketamine',
    'LSD',
    'psilocybin',
    'synthetic cannabinoids',
    'synthetic cathinones',
    'fentanyl',
    'carfentanil',
    'precursor chemicals',
    'pseudoephedrine',

    # Drug equipment and premises
    'drug premises',
    'knowingly take part in',
    'equipment for drug use',
    'drug paraphernalia',
    'implements for administration',
    'implements for manufacture',
    'cannabis seeds',
    'allow premises to be used',
    'permitting drug use on premises',

    # Drug administration
    'administering drug',
    'self-administration',
    'administering to another',
    'causing drug to be taken',

    # Drug driving and use
    'drug driving',
    'presence of prescribed drug',
    'impaired by drug',
    'use in public',
    'public consumption',

    # Proceeds and money
    'proceeds of drug trafficking',
    'money laundering drugs',
    'property suspected proceeds',
    'unexplained wealth',

    # Defences and exceptions
    'therapeutic use',
    'authorised possession',
    'prescription drug',
    'medical practitioner exception',
    'registered health practitioner',
]

# =============================================================================
# OFFENCE CATEGORIES - VIOLENCE
# =============================================================================

CRIM_VIOLENCE = [
    # Assault - general
    'assault',
    'common assault',
    'unlawful assault',
    'assault and battery',
    'battery',
    'technical assault',
    'aggravated assault',
    'assault in company',
    'assault with intent',

    # Assault causing harm
    'assault occasioning actual bodily harm',
    'assault occasioning ABH',
    'ABH',
    'actual bodily harm',
    'assault occasioning bodily harm',
    'assault causing harm',
    'assault causing injury',
    'recklessly causing injury',
    'intentionally causing injury',
    'recklessly causing serious injury',
    'intentionally causing serious injury',

    # Grievous bodily harm
    'grievous bodily harm',
    'GBH',
    'inflict grievous bodily harm',
    'cause grievous bodily harm',
    'maliciously inflict GBH',
    'wounding with intent',
    'wounding',
    'malicious wounding',
    'inflicting bodily harm',
    'really serious harm',
    'serious injury',

    # Specific intent assaults
    'assault with intent to rob',
    'assault with intent to rape',
    'assault with intent to murder',
    'assault with intent to commit serious indictable offence',
    'assault with intent to resist arrest',
    'assault police',
    'assault police in execution of duty',
    'resist police',
    'hinder police',
    'obstruct police',
    'assault correctional officer',
    'assault emergency worker',
    'assault ambulance officer',
    'assault firefighter',

    # Weapons offences related to violence
    'assault with weapon',
    'assault with offensive weapon',
    'assault with dangerous weapon',
    'armed with intent',
    'possess weapon in public',
    'possess prohibited weapon',
    'possess firearm',
    'unauthorised possession of firearm',
    'discharge firearm',
    'discharge firearm in public',
    'shoot with intent',
    'discharge firearm at dwelling',
    'discharge firearm with recklessness',
    'possess shortened firearm',
    'possess unregistered firearm',
    'possess pistol',
    'possess knife in public',
    'custody of knife',
    'offensive weapon',
    'offensive instrument',
    'article with blade or point',

    # Threats and intimidation
    'threaten violence',
    'threaten to kill',
    'threaten to inflict GBH',
    'threaten serious harm',
    'stalking',
    'intimidation',
    'stalking or intimidation',
    'pursue with intent to intimidate',
    'harassment',
    'criminal harassment',
    'threatening behaviour',
    'menacing behaviour',
    'affray',
    'violent disorder',
    'riot',
    'unlawful assembly',

    # Kidnapping and detention
    'kidnapping',
    'kidnap',
    'abduction',
    'false imprisonment',
    'unlawful detention',
    'deprivation of liberty',
    'take and detain',
    'child stealing',
    'taking child',
    'aggravated kidnapping',

    # Domestic violence
    'domestic violence',
    'domestic assault',
    'family violence',
    'intimate partner violence',
    'strangulation',
    'choking',
    'suffocation',
    'non-fatal strangulation',
    'domestic violence related',
    'breach of protection order',
    'breach of intervention order',
    'breach of restraining order',
    'breach of apprehended violence order',
    'breach AVO',
    'breach DVO',
    'contravene family violence order',

    # Protective orders
    'apprehended violence order',
    'AVO',
    'ADVO',
    'APVO',
    'intervention order',
    'restraining order',
    'protection order',
    'family violence intervention order',
    'personal safety intervention order',
    'domestic violence order',
    'DVR protection order',
    'temporary protection order',
    'final protection order',

    # Child abuse
    'child abuse',
    'cruelty to children',
    'ill-treatment of child',
    'failure to provide necessaries',
    'child neglect',
    'abandonment of child',
    'exposing child to harm',

    # Torture and serious violence
    'torture',
    'acts of torture',
    'inflicting severe pain',
    'aggravated violence',
    'extreme violence',
    'mutilation',
    'maiming',

    # One punch offences
    'one punch',
    'coward punch',
    'unlawful striking causing death',
    'assault causing death',
    'king hit',
]

# =============================================================================
# OFFENCE CATEGORIES - TRAFFIC
# =============================================================================

CRIM_TRAFFIC = [
    # Dangerous driving
    'dangerous driving',
    'dangerous operation of vehicle',
    'drive dangerously',
    'dangerous driving causing death',
    'dangerous driving causing grievous bodily harm',
    'dangerous driving causing serious injury',
    'aggravated dangerous driving',
    'culpable driving',
    'culpable driving causing death',
    'reckless driving',
    'menacing driving',
    'furious driving',

    # Drink driving
    'drink driving',
    'drive with prescribed concentration of alcohol',
    'PCA',
    'high range PCA',
    'mid range PCA',
    'low range PCA',
    'special range PCA',
    'exceed prescribed concentration',
    'DUI',
    'drive under influence',
    'drive under influence of alcohol',
    'exceed .05',
    'exceed .08',
    'exceed .15',
    'refuse breath test',
    'refuse breath analysis',
    'fail to provide sample',
    'blood alcohol concentration',
    'BAC',

    # Drug driving
    'drug driving',
    'drive with illicit drug present',
    'drive under influence of drug',
    'prescribed illicit drug',
    'cannabis present in blood',
    'methylamphetamine present',
    'MDMA present',
    'refuse drug test',
    'oral fluid test',
    'impairment by drug',

    # Negligent driving
    'negligent driving',
    'negligent driving occasioning death',
    'negligent driving occasioning GBH',
    'drive without due care',
    'careless driving',
    'driving without reasonable consideration',
    'inattentive driving',

    # License offences
    'drive whilst disqualified',
    'drive whilst suspended',
    'drive whilst licence cancelled',
    'unlicensed driving',
    'never licensed',
    'drive in breach of licence condition',
    'learner driver unaccompanied',
    'P-plate offence',
    'provisional licence breach',

    # Disqualification
    'license disqualification',
    'licence suspension',
    'automatic disqualification',
    'mandatory disqualification',
    'discretionary disqualification',
    'habitual traffic offender',
    'habitual offender declaration',

    # Police pursuits and evading
    'police pursuit',
    'fail to stop',
    'fail to stop for police',
    'evade police',
    'drive recklessly in police pursuit',
    'Skye Law',

    # Street racing and hooning
    'street racing',
    'race on road',
    'speed trial',
    'burnout',
    'loss of traction',
    'aggravated burnout',
    'organised race',
    'hooning',
    'anti-hooning laws',
    'vehicle impoundment',
    'vehicle confiscation',

    # Speed offences
    'speeding',
    'exceed speed limit',
    'excessive speed',
    'low level speeding',
    'moderate speeding',
    'substantial speeding',
    'extreme speeding',

    # Other traffic offences
    'fail to exchange particulars',
    'fail to stop after accident',
    'leave scene of accident',
    'drive manner dangerous',
    'red light offence',
    'drive through red light',
    'cross continuous white line',
    'illegal U-turn',
    'mobile phone while driving',
    'seatbelt offence',
]

# =============================================================================
# SENTENCING TERMINOLOGY AND PRINCIPLES
# =============================================================================

CRIM_SENTENCING = [
    # Sentencing approaches
    'instinctive synthesis',
    'two-stage approach',
    'two-step approach',
    'structured approach to sentencing',
    'guideline judgments',
    'standard non-parole period',
    'SNPP',
    'baseline sentence',
    'starting point',
    'sentencing range',
    'indicative sentence',

    # Sentencing objectives
    'just punishment',
    'adequate punishment',
    'punishment proportionate',
    'general deterrence',
    'specific deterrence',
    'denunciation',
    'community protection',
    'rehabilitation',
    'reparation',
    'restorative justice',
    'totality principle',
    'parity principle',
    'parsimony principle',

    # Aggravating factors
    'aggravating circumstances',
    'aggravating features',
    'objective seriousness',
    'high level of culpability',
    'planned offence',
    'premeditated',
    'breach of trust',
    'abuse of position',
    'vulnerable victim',
    'significant harm',
    'prevalence of offence',
    'offence committed on bail',
    'offence while on parole',
    'prior convictions',
    'criminal history',
    'serious criminal history',
    'multiple victims',
    'sustained offending',
    'course of conduct',

    # Mitigating factors
    'mitigating circumstances',
    'mitigating features',
    'subjective features',
    'remorse',
    'contrition',
    'early plea of guilty',
    'utilitarian value',
    'assistance to authorities',
    'cooperation with police',
    'good character',
    'prior good character',
    'youth',
    'age of offender',
    'lack of prior convictions',
    'prospects of rehabilitation',
    'good rehabilitation prospects',
    'stable employment',
    'family support',
    'mental health condition',
    'cognitive impairment',
    'intellectual disability',
    'addiction',
    'drug dependency',
    'alcohol dependency',
    'deprived background',
    'disadvantaged background',
    'Aboriginal background',
    'Bugmy bar',
    'childhood trauma',

    # Discount for plea
    'discount for guilty plea',
    'utilitarian discount',
    'plea discount',
    'early guilty plea',
    'late guilty plea',
    'plea on indictment',
    'plea at committal',
    'Cameron discount',
    '25% discount',
    'staged discount',

    # Imprisonment types
    'full-time imprisonment',
    'full-time custodial sentence',
    'term of imprisonment',
    'head sentence',
    'aggregate sentence',
    'global sentence',
    'combined sentence',
    'life imprisonment',
    'indefinite sentence',
    'indeterminate sentence',
    'standard non-parole period',
    'minimum term',
    'non-parole period',
    'NPP',
    'parole period',
    'balance of term',

    # Concurrent and cumulative
    'concurrent sentences',
    'serve concurrently',
    'wholly concurrent',
    'partly concurrent',
    'cumulative sentences',
    'serve cumulatively',
    'wholly cumulative',
    'partly cumulative',
    'consecutive sentences',

    # Community orders
    'intensive correction order',
    'ICO',
    'community correction order',
    'CCO',
    'community service order',
    'CSO',
    'community based order',
    'CBO',
    'good behaviour bond',
    'section 10 dismissal',
    'section 10 bond',
    'conditional release order',
    'CRO',
    'recognizance',
    'recognisance',
    'surety',
    'suspended sentence',
    'wholly suspended',
    'partly suspended',
    'home detention',

    # Fines and restitution
    'fine',
    'monetary penalty',
    'penalty units',
    'maximum fine',
    'compensation order',
    'restitution order',
    'reparation',
    'victim compensation',

    # Parole
    'parole',
    'release on parole',
    'parole eligibility',
    'parole application',
    'parole board',
    'State Parole Authority',
    'Adult Parole Board',
    'conditions of parole',
    'parole breach',
    'parole revocation',
    'serious violent offender',
    'serious sex offender',

    # Special sentences
    'preventive detention',
    'continuing detention order',
    'extended supervision order',
    'ESO',
    'supervision order',
    'post-sentence detention',
    'dangerous offender',
    'serious danger to community',

    # Time calculations
    'pre-sentence custody',
    'time served',
    'time in custody',
    'backdating sentence',
    'declaration of pre-sentence detention',
    'rounding up',
    'rounding down',

    # Sentencing procedures
    'victim impact statement',
    'VIS',
    'assessment report',
    'pre-sentence report',
    'psychological report',
    'psychiatric report',
    'medical report',
    'sentencing submissions',
    'objective circumstances',
    'subjective circumstances',
    'Form 1',
    'schedule of offences',
    'taking offences into account',
    'asked to be taken into account',
]

# =============================================================================
# CRIMINAL PROCEDURE
# =============================================================================

CRIM_PROCEDURE = [
    # Arrest and charging
    'arrest',
    'arrest without warrant',
    'arrest warrant',
    'lawful arrest',
    'unlawful arrest',
    'false imprisonment by police',
    'charge',
    'charging',
    'lay charge',
    'prefer charge',
    'withdraw charge',
    'alternative charge',
    'substitute charge',
    'additional charge',

    # Bail
    'bail',
    'bail application',
    'grant bail',
    'refuse bail',
    'conditional bail',
    'unconditional bail',
    'bail conditions',
    'bail undertaking',
    'surety',
    'security for bail',
    'cash bail',
    'bail breach',
    'fail to appear',
    'unacceptable risk',
    'show cause',
    'presumption against bail',
    'presumption in favour of bail',
    'exceptional circumstances',
    'bail review',
    'Supreme Court bail',

    # Court proceedings
    'mention',
    'first mention',
    'arraignment',
    'plea',
    'committal',
    'committal hearing',
    'hand-up committal',
    'committal proceedings',
    'ex officio indictment',
    'indictment',
    'presentment',
    'prefer indictment',
    'trial',
    'judge alone trial',
    'jury trial',
    'summary trial',

    # Evidence and procedure
    'beyond reasonable doubt',
    'burden of proof',
    'standard of proof',
    'onus of proof',
    'reverse onus',
    'evidential burden',
    'legal burden',
    'prima facie case',
    'no case to answer',
    'no case submission',
    'directed verdict',
    'directed acquittal',

    # Verdicts
    'guilty verdict',
    'not guilty verdict',
    'alternative verdict',
    'special verdict',
    'not guilty by reason of mental impairment',
    'NGMI',
    'unfit to plead',
    'unfit to stand trial',
    'hung jury',
    'disagreement of jury',
    'majority verdict',
    'unanimous verdict',

    # Jurisdiction
    'summary offence',
    'indictable offence',
    'strictly indictable',
    'table offence',
    'either way offence',
    'election for summary',
    'election for trial',
    'jurisdiction',
    'territorial jurisdiction',

    # Disclosure and procedure
    'disclosure',
    'prosecution disclosure',
    'defence disclosure',
    'hand-up brief',
    'committal brief',
    'alibi notice',
    'expert evidence notice',

    # Police powers
    'search warrant',
    'crime scene warrant',
    'covert search warrant',
    'telephone intercept',
    'listening device',
    'surveillance device',
    'controlled operation',
    'assumed identity',
    'police questioning',
    'record of interview',
    'ERISP',
    'right to silence',
    'caution',
    'police caution',

    # Proceeds of crime
    'proceeds of crime',
    'restraining order',
    'forfeiture order',
    'pecuniary penalty order',
    'unexplained wealth order',
    'literary proceeds order',
    'property tracking',
    'confiscation',
    'asset forfeiture',

    # Victims
    'victim',
    'complainant',
    'protected witness',
    'special witness',
    'vulnerable witness',
    'child witness',
    'CCTV evidence',
    'pre-recorded evidence',
    'support person',
    'screen in court',
    'victim impact statement',

    # Organized crime
    'criminal organization',
    'declared organization',
    'outlaw motorcycle gang',
    'OMCG',
    'organized crime',
    'enterprise crime',
    'unexplained wealth',
    'consorting',
    'criminal association',
]

# =============================================================================
# CRIMINAL APPEALS
# =============================================================================

CRIM_APPEALS = [
    # General appeal terms
    'criminal appeal',
    'appeal against conviction',
    'appeal against sentence',
    'appeal by Crown',
    'Crown appeal',
    'appeal by Attorney-General',
    'Director of Public Prosecutions appeal',
    'DPP appeal',
    'prosecution appeal',

    # Grounds of appeal
    'ground of appeal',
    'grounds of appeal',
    'unsafe conviction',
    'unreasonable verdict',
    'unsatisfactory verdict',
    'verdict unreasonable',
    'cannot be supported by evidence',
    'miscarriage of justice',
    'substantial miscarriage of justice',
    'wrong decision on question of law',
    'error of law',
    'misdirection to jury',
    'non-direction to jury',
    'improper admission of evidence',
    'improper rejection of evidence',
    'irregularity in trial',
    'denial of procedural fairness',

    # Sentence appeals
    'manifestly excessive',
    'manifest excess',
    'manifestly inadequate',
    'crushing sentence',
    'error in sentencing discretion',
    'House v The King error',
    'sentencing error',
    'wrong in principle',
    'improper exercise of discretion',

    # Fresh evidence
    'fresh evidence',
    'new evidence',
    'additional evidence',
    'evidence not available at trial',
    'credible fresh evidence',

    # Appeal outcomes
    'allow appeal',
    'dismiss appeal',
    'quash conviction',
    'set aside conviction',
    'affirm conviction',
    'uphold conviction',
    'order new trial',
    'retrial',
    'vary sentence',
    'reduce sentence',
    'increase sentence',
    'substitute different sentence',
    'resentence',

    # Procedural matters
    'leave to appeal',
    'application for leave',
    'extension of time',
    'out of time',
    'notice of appeal',
    'grounds of appeal',
    'appeal book',
    'written submissions',
    'oral argument',

    # High Court appeals
    'special leave',
    'special leave application',
    'question of law',
    'matter of general importance',
    'departure from previous authority',
    'conflicting decisions',

    # Proviso
    'proviso',
    'no substantial miscarriage',
    'no miscarriage of justice',
    'conviction inevitable',
    'evidence of such strength',
]

# =============================================================================
# CRIMINAL DEFENCES
# =============================================================================

CRIM_DEFENCES = [
    # Self-defence
    'self-defence',
    'self defence',
    'defence of person',
    'defence of property',
    'defence of another',
    'reasonable force',
    'proportionate response',
    'excessive force',
    'excessive self-defence',
    'belief in necessity',
    'honest and reasonable belief',
    'perceived threat',
    'imminent threat',
    'immediacy of threat',
    'retreat',
    'duty to retreat',
    'no duty to retreat',
    'battered woman syndrome',
    'defensive homicide',

    # Duress
    'duress',
    'compulsion',
    'threat of death',
    'threat of serious harm',
    'no reasonable alternative',
    'proportionality of response',
    'immediacy of threat duress',
    'availability of police protection',
    'duress not available for murder',

    # Necessity
    'necessity',
    'lesser of two evils',
    'emergency',
    'urgent situation',
    'no reasonable alternative necessity',

    # Mental impairment
    'mental impairment',
    'mental illness',
    'disease of the mind',
    'defect of reason',
    'M\'Naghten rules',
    'nature and quality of act',
    'knowing act was wrong',
    'did not know wrongness',
    'insanity',
    'insane at time of offence',
    'special verdict',
    'not guilty mental impairment',

    # Automatism
    'automatism',
    'involuntary act',
    'sane automatism',
    'insane automatism',
    'unconscious act',
    'reflex action',
    'epileptic seizure',
    'diabetic episode',
    'hypoglycemia',
    'sleepwalking',
    'parasomnia',

    # Intoxication
    'intoxication',
    'self-induced intoxication',
    'involuntary intoxication',
    'intoxication and specific intent',
    'intoxication and basic intent',
    'negating specific intent',
    'drink or drug affected',

    # Mistake
    'mistake of fact',
    'honest and reasonable mistake',
    'factual error',
    'negating mens rea',
    'claim of right',
    'honest belief in consent',

    # Provocation
    'provocation',
    'loss of self-control',
    'sudden and temporary loss',
    'ordinary person test',
    'provoked response',
    'proportionality provocation',
    'words alone',
    'cumulative provocation',
    'abolished provocation',

    # Diminished responsibility
    'diminished responsibility',
    'substantial impairment',
    'abnormality of mental functioning',
    'partial defence',
    'reduce murder to manslaughter',

    # Other defences
    'consent',
    'lawful authority',
    'lawful excuse',
    'honest claim of right',
    'statutory defence',
    'lawful correction',
    'reasonable chastisement',
    'medical treatment',
    'surgical operation',
    'sporting activity',
    'social utility',
]

# =============================================================================
# MENS REA AND CRIMINAL RESPONSIBILITY
# =============================================================================

CRIM_MENS_REA = [
    # Mental elements
    'mens rea',
    'guilty mind',
    'mental element',
    'fault element',
    'criminal intent',
    'state of mind',

    # Intention
    'intention',
    'intent',
    'specific intent',
    'basic intent',
    'direct intention',
    'oblique intention',
    'purposive intent',
    'conditional intent',
    'transferred intent',
    'doctrine of transferred malice',

    # Knowledge
    'knowledge',
    'actual knowledge',
    'constructive knowledge',
    'wilful blindness',
    'deliberate ignorance',
    'shutting eyes',
    'Connelly knowledge',
    'knowledge or belief',

    # Recklessness
    'recklessness',
    'Cunningham recklessness',
    'subjective recklessness',
    'awareness of risk',
    'unjustifiable risk',
    'substantial risk',
    'unreasonable risk',

    # Negligence
    'negligence',
    'criminal negligence',
    'gross negligence',
    'objective test',
    'reasonable person',
    'fell below standard',
    'failure to foresee',

    # Strict liability
    'strict liability',
    'absolute liability',
    'no mens rea required',
    'regulatory offence',
    'public welfare offence',

    # Causation
    'causation',
    'factual causation',
    'legal causation',
    'but for test',
    'substantial cause',
    'operating and substantial cause',
    'novus actus interveniens',
    'intervening act',
    'breaking causal chain',
    'reasonable foreseeability',

    # Voluntariness
    'voluntary act',
    'voluntariness',
    'conscious control',
    'willed act',
    'involuntary conduct',
    'reflex action',
]

# =============================================================================
# LANDMARK CRIMINAL CASES
# =============================================================================

CRIMINAL_CASES = [
    # High Court - Homicide
    'Royall v The Queen (1991) 172 CLR 378',
    'R v Crabbe (1985) 156 CLR 464',
    'Stingel v The Queen (1990) 171 CLR 312',
    'Zecevic v DPP (Vic) (1987) 162 CLR 645',
    'Van Den Hoek v The Queen (1986) 161 CLR 158',
    'Masciantonio v The Queen (1995) 183 CLR 58',
    'Wilson v The Queen (1992) 174 CLR 313',
    'Pemble v The Queen (1971) 124 CLR 107',

    # High Court - Mens rea and elements
    'He Kaw Teh v The Queen (1985) 157 CLR 523',
    'Vallance v The Queen (1961) 108 CLR 56',
    'Ryan v The Queen (1967) 121 CLR 205',
    'R v Falconer (1990) 171 CLR 30',
    'Thomas v The Queen (1937) 59 CLR 279',
    'Stapleton v The Queen (1952) 86 CLR 358',
    'Timbu Kolian v The Queen (1968) 119 CLR 47',
    'CTM v The Queen (2008) 236 CLR 440',

    # High Court - Sentencing
    'Markarian v The Queen (2005) 228 CLR 357',
    'Muldrock v The Queen (2011) 244 CLR 120',
    'Barbaro v The Queen (2014) 253 CLR 58',
    'Hili v The Queen (2010) 242 CLR 520',
    'Bugmy v The Queen (2013) 249 CLR 571',
    'Cameron v The Queen (2002) 209 CLR 339',
    'Wong v The Queen (2001) 207 CLR 584',
    'Mill v The Queen (1988) 166 CLR 59',

    # High Court - Appeals
    'Barca v The Queen (1975) 133 CLR 82',
    'M v The Queen (1994) 181 CLR 487',
    'Weiss v The Queen (2005) 224 CLR 300',
    'Trawl Industries v Effem Foods (1992) 27 NSWLR 326',

    # High Court - Evidence
    'Pfennig v The Queen (1995) 182 CLR 461',
    'Phillips v The Queen (2006) 225 CLR 303',
    'IMM v The Queen (2016) 257 CLR 300',
    'R v BD (1997) 94 A Crim R 131',

    # State Courts
    'R v Porter (1933) 55 CLR 182',
    'R v Kalache [2000] NSWCCA 2',
    'DPP v Sherna [2009] VSCA 50',
    'Morgan v The Queen (1993) 30 NSWLR 543',
    'R v Lavender (2005) 222 CLR 67',
]

# =============================================================================
# COMBINED CRIMINAL KEYWORDS DICTIONARY
# =============================================================================

CRIMINAL_KEYWORDS = {
    'Crim_Homicide': CRIM_HOMICIDE,
    'Crim_Sexual': CRIM_SEXUAL,
    'Crim_Property': CRIM_PROPERTY,
    'Crim_Drugs': CRIM_DRUGS,
    'Crim_Violence': CRIM_VIOLENCE,
    'Crim_Traffic': CRIM_TRAFFIC,
    'Crim_Sentencing': CRIM_SENTENCING,
    'Crim_Procedure': CRIM_PROCEDURE,
    'Crim_Appeals': CRIM_APPEALS,
    'Crim_Defences': CRIM_DEFENCES,
    'Crim_Mens_Rea': CRIM_MENS_REA,
}

# =============================================================================
# STATISTICS
# =============================================================================

def get_statistics():
    """Generate statistics about the criminal law taxonomy."""
    total_keywords = sum(len(keywords) for keywords in CRIMINAL_KEYWORDS.values())
    total_legislation = sum(len(acts) for acts in CRIMINAL_LEGISLATION.values())
    total_cases = len(CRIMINAL_CASES)

    stats = {
        'total_keywords': total_keywords,
        'total_legislation': total_legislation,
        'total_cases': total_cases,
        'total_items': total_keywords + total_legislation + total_cases,
        'categories': len(CRIMINAL_KEYWORDS),
        'jurisdictions': len(CRIMINAL_LEGISLATION),
        'breakdown': {
            category: len(keywords)
            for category, keywords in CRIMINAL_KEYWORDS.items()
        }
    }

    return stats

# Export all
__all__ = [
    'CRIMINAL_KEYWORDS',
    'CRIMINAL_LEGISLATION',
    'CRIMINAL_CASES',
    'CRIM_HOMICIDE',
    'CRIM_SEXUAL',
    'CRIM_PROPERTY',
    'CRIM_DRUGS',
    'CRIM_VIOLENCE',
    'CRIM_TRAFFIC',
    'CRIM_SENTENCING',
    'CRIM_PROCEDURE',
    'CRIM_APPEALS',
    'CRIM_DEFENCES',
    'CRIM_MENS_REA',
    'get_statistics',
]

# Print statistics when module is run directly
if __name__ == '__main__':
    stats = get_statistics()
    print("Criminal Law Taxonomy Statistics")
    print("=" * 50)
    print(f"Total Keywords: {stats['total_keywords']}")
    print(f"Total Legislation: {stats['total_legislation']}")
    print(f"Total Cases: {stats['total_cases']}")
    print(f"Total Items: {stats['total_items']}")
    print(f"\nCategories: {stats['categories']}")
    print(f"Jurisdictions: {stats['jurisdictions']}")
    print("\nKeyword Breakdown by Category:")
    print("-" * 50)
    for category, count in stats['breakdown'].items():
        print(f"  {category}: {count}")
