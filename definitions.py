import os


class PathsDir:
    """
    Directory paths
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
    DATA = os.path.join(BASE_DIR, 'data')
    MISC = os.path.join(PROJECT_ROOT, 'misc')
    OUTPUT = os.path.join(PROJECT_ROOT, 'output')
    RECEPTORS = os.path.join(DATA, 'receptors')
    WORD_DOCS = os.path.join(PROJECT_ROOT, 'word_docs')
    CHARTS = os.path.join(DATA, 'charts')
    LOOKUPS = os.path.join(PROJECT_ROOT, 'lookups')
    BRES = os.path.join(RECEPTORS, 'bres')
    OCC = os.path.join(RECEPTORS, 'occupation')
    SKILLS = os.path.join(RECEPTORS, 'skills')
    UNEMPL = os.path.join(RECEPTORS, 'unemployment')


class PathsFile:
    """
    File paths
    """
    LOOKUP = os.path.join(PathsDir.LOOKUPS, 'lookup_lad_rgn_cmba_ctry_190918.csv')
    AREACODE_LOOKUP = os.path.join(PathsDir.LOOKUPS, 'areacode_lookup.tsv')
    AREACD_LOOKUP_APS = os.path.join(PathsDir.LOOKUPS, 'areacode_lookup_aps.tsv')

    WORD_TEMPLATE = os.path.join(PathsDir.WORD_DOCS, 'template.docx')

    MYEDE_TSV = os.path.join(PathsDir.MISC, 'myede_2017.tsv')
    SNPP_TSV = os.path.join(PathsDir.RECEPTORS, 'snpp_2016.tsv')
    AFFORD_XLSX = os.path.join(PathsDir.RECEPTORS, 'affordability_2017.xlsx')

    SNPP_CHART = os.path.join(PathsDir.CHARTS, 'snpp_pop_breakdown.png')
    AFFORD_CHART = os.path.join(PathsDir.CHARTS, 'afford_ratios.png')
    BRES_CHART = os.path.join(PathsDir.CHARTS, 'bres_time_series.png')
    UNEMPL_CHART = os.path.join(PathsDir.CHARTS, 'unemployment_time_series.png')

    WORD_OUTPUT = os.path.join(PathsDir.OUTPUT, 'output.docx')
    EXCEL_OUTPUT = os.path.join(PathsDir.OUTPUT, 'baseline_analysis.xlsx')

    DESKTOP = os.path.join(os.environ['USERPROFILE'], 'Desktop', 'baseline_test.csv')


class LookUp:
    """
    Column headers and dict keys related to the geography lookup
    """
    LAD_CD = 'LAD17CD'
    LAD_NM = 'LAD17NM'
    ctry_cd = 'CTRY17CD'
    ctry_nm = 'CTRY17NM'
    rgn_cd = 'RGN15CD'
    rgn_nm =  'RGN15NM'
    cauth_cd = 'CAUTH17CD'
    cauth_nm = 'CAUTH17NM'


class Nom:
    """
    Column headers of Nomis data
    """
    # inherent names
    DATE = 'DATE'
    INDUSTRY = 'industry'
    VALUE = 'OBS_VALUE'
    AREA = 'GEOGRAPHY_NAME'
    CODE = 'GEOGRAPHY_CODE'
    TYPE = 'GEOGRAPHY_TYPE'
    # created names
    AREA_NM = 'area_name'
    AREA_TYPE = 'area_type'
    AREA_CD = 'area_code'
    AREA_NM_LOWER = 'area_name_lower'
    SIC_CODE = 'sic_code'
    SECTOR = 'sector'


class Pop:
    """
    Column headers or dict keys specific to population estimates and projections
    """
    age = 'C_AGE_NAME'
    value = 'OBS_VALUE'
    age_band = 'age_band'
    total_pop = 'total_pop'
    total_pop_past = 'total_pop_past'
    pop_bands = 'pop_bands'
    pop_bands_past = 'pop_bands_past'
    pop_bands_pct = 'pop_bands_pct'
    pop_bands_past_pct = 'pop_bands_past_pct'
    pop_chg = 'pop_chg'
    pop_chg_pct = 'pop_chg_pct'
    pop_bands_chg = 'pop_bands_chg'
    pop_bands_chg_pct = 'pop_bands_chg_pct'


class Aff:
    """
    Column headers or dict keys specific to affordability
    """
    AFF_RATIO = 'affordability_ratio'
    AFF_RATIO_TM10 = 'afford_ratio_t-10'
    AFF_RATIO_CHG = 'aff_rat_chg'


class Bres:
    """
    Column headers or dict keys specific to BRES
    """
    EMPL = 'empl'
    EMPL_PAST = 'empl_past'
    EMPL_CHG = 'empl_chg'
    EMPL_CHG_PCT = 'empl_chg_pct'

    EMPL_FMT = 'empl_fmt'
    EMPL_PAST_FMT = 'empl_past_fmt'
    EMPL_CHG_FMT = 'empl_chg_fmt'
    EMPL_CHG_PCT_FMT = 'empl_chg_pct_fmt'


class Aps:
    """
    Column headers or dict keys specific to APS
    """
    VAL_TYPE = 'value type'
    DATE = 'date'
    PCT = 'Percent'
    VAR = 'Variable'
    END_DATE = 'end_date'

    UNEMPL_RT = 'unempl_rt'
    UNEMPL_AVG = 'unempl_avg'

    OCC_HIGH_SKILL = 'occ_high_skill'
    OCC = 'occupation'
    ORDER = 'order'

    SKILL = 'skill'
    PCT_LEVEL4 = 'pct_level4+'


class AgeBands:
    youth = '0-15'
    working_age = '16-64'
    retirement = '65+'
    bands = [youth, working_age, retirement]


# dictionary of receptors to be which can be included in the baseline
receptors = {
    'myede': ['Mid-year population estimates'],
    'snpp': ['Sub-national population projections'],
    'bres': ['Employment'],
    'unempl': ['Unemployment'],
    'occ': ['Occupational profile'],
    'skills': ['Proportion highly skilled workers'],
    'afford': ['Affordability'],
}


class DocStyles:
    # text styles
    heading5 = 'Heading 5'
    heading4 = 'Heading 4'
    heading3 = 'Heading 3'
    heading2 = 'Heading 2'

    # table styles
    placeholder = 'Placeholder'
    table = 'Table New'

    # table text styles
    tableTitle = 'Table Title'
    tableSource = 'Table Source'
    tableText = 'Table Text'
    tableNumber = 'Table Number'
    tableHeading = 'Table Heading'

    # figure text styles
    figureTitle = 'Figure Title'
    normalFigures = 'NormalFigures'
    figureSource = 'Figure Source'


class FootNotes:
    """
    footnotes and sources usinged in figures and tables
    """
    MYEDE = 'Source: ONS (2022), Mid-year population estimates'
    SNPP = 'Source: ONS (2018), Subnational population projections'
    AFF = 'Source: ONS, Ratio of house price to residence-based earnings, 2018'
    BRES = 'Source: ONS (2017), Business Register and Employment Survey'
    APS = 'Source: ONS (2018), Annual Population Survey'

class NomisAPI:
    """
    Nomis API links
    """
    myede_api = 'https://www.nomisweb.co.uk/api/v01/dataset/NM_2002_1.data.tsv?geography=1879048193...1879048573,1879048583,1879048574...1879048582&date=latestMINUS10,latest&gender=0&c_age=101...191&measures=20100&uid=0xe604927b6c64b9afa87eba633d7a2f7d1cc4a338'