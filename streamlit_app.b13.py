import streamlit as st
import pandas as pd
import math

VAT_RATE = 0.18
YEARS_OF_COMPARISON = 12
TAG_DEPOSIT = "פיקדון"
TAG_ENTRY_FEE = "דמי כניסה"
TAG_MONTHLY_ONLY = "תשלום חודשי בלבד"
TAG_NO_OFFER = "ללא הצעה שניה להשוואה"
TAG_MONTHLY_PAYMENT_PROMPMT = "תשלום חודשי שוטף (דמי שימוש / אחזקה):"

if 'Do_Calc_Indicator' not in st.session_state:
    st.session_state.Do_Calc_Indicator = False

# Apply RTL styling to the entire app, except for number inputs
st.markdown("""
<style>
body, html {
    direction: RTL;
    unicode-bidi: bidi-override;
    text-align: left;
}
p, div, input, label, h1, h2, h3, h4, h5, h6 {
    direction: RTL;
    unicode-bidi: bidi-override;
    text-align: left;
}
            
div[data-testid="stNumberInput"] input {
        direction: LTR;
        text-align: left;
}

</style>
""", unsafe_allow_html=True)

### Initialize session state on first run ###
def initialize_first_run():
    st.session_state.ST_Off_Name = [None, None]
    st.session_state.ST_Off_Type = [None, None]
    st.session_state.ST_Off_Deposit = [None, None]
    st.session_state.ST_Off_Deposit_Decreas = [None, None]
    st.session_state.ST_Off_VAT_on_Deposit = [None, None]
    st.session_state.ST_Off_Deposit_Min_Refund = [None, None]
    st.session_state.ST_Off_Monthly_Payment = [None, None]
    st.session_state.ST_Off_Entry_Fee = [None, None]

    st.session_state.First_Init_Done = True

### Form for getting offers' details from user ###
@st.fragment()
def Offers_Form():

    col1, col2 = st.columns(2)

    # נתוני הצעה ראשונה להשוואה
    with col1:
        with st.container(border=True):
            st.header("הצעה ראשונה")
            get_offer_input(0, False)

    # נתוני הצעה שניה להשוואה
    with col2:
        with st.container(border=True):
            st.header("הצעה שניה")
            get_offer_input(1, True)

# single offer input form 
def get_offer_input(offer_num, optional_offer):
    if optional_offer:
        Off_Type_Options = [TAG_NO_OFFER, TAG_DEPOSIT, TAG_ENTRY_FEE, TAG_MONTHLY_ONLY]
        First_Off_Type = st.selectbox("סוג הצעה:", Off_Type_Options,
                                    index=0,
                                    key=("Off_Type_" + str(offer_num)))
        st.session_state.ST_Off_Type[offer_num] = First_Off_Type

        if First_Off_Type == TAG_NO_OFFER:
            return
        
    else:First_Off_Type = st.selectbox("סוג הצעה:", [TAG_DEPOSIT, TAG_ENTRY_FEE, TAG_MONTHLY_ONLY],
                                index=0,
                                key=("Off_Type_" + str(offer_num)))
    st.session_state.ST_Off_Type[offer_num] = First_Off_Type

    First_Off_Name = st.text_input("שם ההצעה:", key=("Off_Name_" + str(offer_num)))
    st.session_state.ST_Off_Name[offer_num] = First_Off_Name
    
    if First_Off_Type == TAG_DEPOSIT:
        First_Off_Deposit = st.number_input("סכום הפיקדון:", min_value=0, step=100000,
                                            value=1500000,
                                            format="%0.0i",
                                            key="Off_Deposit" + str(offer_num)) 
        st.session_state.ST_Off_Deposit[offer_num] = First_Off_Deposit

        First_Off_Deposit_Decreas = st.number_input("אחוז הפחתת פיקדון שנתי (%)", min_value=1.0,
                                                    max_value=30.0, step=0.25,
                                                    value=4.0,
                                                    key="Off_Deposit_Decreas" + str(offer_num)) / 100
        st.session_state.ST_Off_Deposit_Decreas[offer_num] = First_Off_Deposit_Decreas
        First_Off_VAT_on_Deposit = st.checkbox('האם מוסיפים מע"מ על שחיקת הפיקדון השנתית?', value=True,
                                            key="Off_VAT_on_Deposit" + str(offer_num))
        st.session_state.ST_Off_VAT_on_Deposit[offer_num] = First_Off_VAT_on_Deposit
        First_Off_Deposit_Min_Refund = st.number_input("אחוז שחיקה מקסימלי של הפיקדון (%)",
                                                        min_value=10.0, max_value=90.0, 
                                                        value=36.0,
                                                        key=("Off_Deposit_Min_Refund" + str(offer_num)),
                                                        step=1.0) / 100
        st.session_state.ST_Off_Deposit_Min_Refund[offer_num] = First_Off_Deposit_Min_Refund
        First_Off_Monthly_Payment = st.number_input(TAG_MONTHLY_PAYMENT_PROMPMT, min_value=0,
                                                    value=8000,
                                                    key="First_Off_Monthly_Payment" + str(offer_num),
                                                    step=100, format="%0.0i")
        st.session_state.ST_Off_Monthly_Payment[offer_num] = First_Off_Monthly_Payment

    elif First_Off_Type == TAG_ENTRY_FEE: 
        First_Off_Entry_Fee = st.number_input("סכום דמי הכניסה:", min_value=0, step=100,
                                            format="%0.0i",key="Off_Entry_Fee" + str(offer_num))
        st.session_state.ST_Off_Entry_Fee[offer_num] = First_Off_Entry_Fee
        First_Off_Deposit_Decreas = st.number_input("אחוז הפחתת דמי כניסה חודשי (%)", min_value=0.1, max_value=3.0, step=0.1,
                                                    key="Off_Deposit_Decreas" + str(offer_num)) / 100
        st.session_state.ST_Off_Deposit_Decreas[offer_num] = First_Off_Deposit_Decreas
        First_Off_VAT_on_Deposit = st.checkbox('האם מוסיפים מע"מ על שחיקת הפיקדון החודשית?', value=True,
                                            key="Off_VAT_on_Deposit" + str(offer_num))
        st.session_state.ST_Off_VAT_on_Deposit[offer_num] = First_Off_VAT_on_Deposit
        First_Off_Monthly_Payment = st.number_input(TAG_MONTHLY_PAYMENT_PROMPMT, min_value=0, step=100,
                                                    format="%0.0i", key="Off_Monthly_Payment" + str(offer_num))
        st.session_state.ST_Off_Monthly_Payment[offer_num] = First_Off_Monthly_Payment

    elif First_Off_Type == TAG_MONTHLY_ONLY:
        First_Off_Monthly_Payment = st.number_input(TAG_MONTHLY_PAYMENT_PROMPMT, min_value=0, step=100,
                                                    format="%0.0i", key ="Off_Monthly_Payment" + str(offer_num)) 
        st.session_state.ST_Off_Monthly_Payment[offer_num] = First_Off_Monthly_Payment

def do_calc_indicator():
    st.session_state.Do_Calc_Indicator = True

### Offer calculations functions ###
def prepare_offer_data(i, effective_VAT_rate):
    if st.session_state.ST_Off_Type[i] == TAG_DEPOSIT:
        drr = (st.session_state.ST_Off_Deposit_Decreas[i] / 100) * (1+ effective_VAT_rate)
    elif st.session_state.ST_Off_Type[i] == TAG_ENTRY_FEE:
        drr = ((st.session_state.ST_Off_Deposit_Decreas[i]*12)/100) * (1+ effective_VAT_rate)
        st.session_state.ST_Off_Deposit_Min_Refund[i] = 0
        st.session_state.ST_Off_Deposit[i] = st.session_state.ST_Off_Entry_Fee[i]
    else:
        st.session_state.ST_Off_Deposit[i] = 0
        st.session_state.ST_Off_Deposit_Decreas[i] = 0
        st.session_state.ST_Off_Deposit_Min_Refund[i] = 0
        drr = 0.0
    return drr             

def year_pv_factor(year, month_interest):
    return (1 - math.pow(1 + month_interest, -year * 12)) / month_interest

def deposit_returned(deposit, drr, min_refund, year):
    deposit_r = max(
        deposit * (1 - drr * year),
        deposit * min_refund
    )
    return deposit_r if deposit_r > 1 else 0

def build_pv_table(Off_Deposit, Off_Deposit_Decreas, Off_Deposit_Min_Refund,
                   Off_Monthly_Payment, Off_DRR, month_interest):
    pv_table = []
    for y in range(1, YEARS_OF_COMPARISON + 1):
        pv_factor_year_y = year_pv_factor(y, month_interest)
        pv_rent_year_y = Off_Monthly_Payment * pv_factor_year_y * (1 + month_interest)
        deposit_returned_year_y = deposit_returned(Off_Deposit, Off_DRR, Off_Deposit_Min_Refund, y)
        pv_deposit_returned_year_y = deposit_returned_year_y / math.pow(1 + month_interest, y * 12)
        pv_total_year_y = Off_Deposit + pv_rent_year_y - pv_deposit_returned_year_y
        pv_monthly_avarage_year_y = pv_total_year_y / (y * 12)
        
        pv_table.append({
            'Year': y,
            'Deposit Returned': int(deposit_returned_year_y),
            "PV Deposit Returned": int(pv_deposit_returned_year_y),
            "PV Rent": int(pv_rent_year_y),
            "PV Total": int(pv_total_year_y),
            "PV Monthly Avarage": int(pv_monthly_avarage_year_y)
        })
    return pv_table



# Define a function to highlight the lowest value in the two columns for each row
def highlight_lowest(row):
    styles = [''] * len(row)
    # Find the positions of the two target columns
    col_a = (deal0_name, 'סך עלות דיור מוגן בערך נוכחי')
    col_b = (deal1_name, 'סך עלות דיור מוגן בערך נוכחי')
    # Compare values
    if col_a in row.index and col_b in row.index:
        if row[col_a] < row[col_b]:
            styles[row.index.get_loc(col_a)] = 'background-color: #d0f0c0'
        else:
            styles[row.index.get_loc(col_b)] = 'background-color: #d0f0c0'
    return styles

### MAIN PROGRAM ###

if 'First_Init_Done' not in st.session_state:
    initialize_first_run()
    
st.title("השוואה כלכלית של הצעות לדיור מוגן")



Offers_Form()

col1, col2, col3 = st.columns(3)
with col1:
    Interest_Rate = st.number_input("ריבית שנתית לחישוב (%):",
                                min_value=1.0, max_value=10.0, value=4.0, step=0.25,
                                format="%0.2f") / 100
    
col1, col2, col3 = st.columns(3)
with col1:
    st.button("לחץ לביצוע חישוב והשוואה", on_click=do_calc_indicator, type="primary")
with col2:
    show_details = st.toggle("הצג נתונים מפורטים", value=False, key="show_detailed_data")

if st.session_state.Do_Calc_Indicator == True:
    
    # Check if second offer exists
    second_offer_exists = st.session_state.ST_Off_Type[1] != TAG_NO_OFFER

    # ביצוע והדפסה של השוואה
    month_interest = math.pow(1 + Interest_Rate, 1/12) - 1
        
    # Calculate first offer
    effective_VAT_rate0 = VAT_RATE if st.session_state.ST_Off_VAT_on_Deposit[0] else 0
    drr0 = prepare_offer_data(0, effective_VAT_rate0)
    off0_results = build_pv_table(
        st.session_state.ST_Off_Deposit[0],
        st.session_state.ST_Off_Deposit_Decreas[0],
        st.session_state.ST_Off_Deposit_Min_Refund[0],
        st.session_state.ST_Off_Monthly_Payment[0],
        drr0 * 100,
        month_interest
    )

    if second_offer_exists:
        effective_VAT_rate1 = VAT_RATE if st.session_state.ST_Off_VAT_on_Deposit[1] else 0
        drr1 = prepare_offer_data(1, effective_VAT_rate1)
        off1_results = build_pv_table(
            st.session_state.ST_Off_Deposit[1],
            st.session_state.ST_Off_Deposit_Decreas[1],
            st.session_state.ST_Off_Deposit_Min_Refund[1],
            st.session_state.ST_Off_Monthly_Payment[1],
            drr1 * 100,
            month_interest
        )

    # Combine rows
    combined_rows = []
    if second_offer_exists:
        for a, b in zip(off0_results, off1_results):
            combined_rows.append([
                a['Year'],
                a['Deposit Returned'], a['PV Deposit Returned'], a['PV Rent'], a['PV Total'], a['PV Monthly Avarage'],
                b['Deposit Returned'], b['PV Deposit Returned'], b['PV Rent'], b['PV Total'], b['PV Monthly Avarage']
            ])
    else:
        for a in off0_results:
            combined_rows.append([
                a['Year'],
                a['Deposit Returned'], a['PV Deposit Returned'], a['PV Rent'], a['PV Total'], a['PV Monthly Avarage']
            ])

    # Deal names
    deal0_name = st.session_state.ST_Off_Name[0] or "הצעה ראשונה"
    deal1_name = st.session_state.ST_Off_Name[1] or "הצעה שניה"

    # Define columns
    if second_offer_exists:
        columns = pd.MultiIndex.from_tuples([
            ('', 'שנה'),
            (deal0_name, 'פיקדון שיוחזר'),
            (deal0_name, 'ערך נוכחי של פיקדון שיוחזר'),
            (deal0_name, 'ערך נוכחי של תשלומים חודשיים'),
            (deal0_name, 'סך עלות דיור מוגן בערך נוכחי'),
            (deal0_name, 'ממוצע עלות לחודש בערך נוכחי'),
            (deal1_name, 'פיקדון שיוחזר'),
            (deal1_name, 'ערך נוכחי של פיקדון שיוחזר'),
            (deal1_name, 'ערך נוכחי של תשלומים חודשיים'),
            (deal1_name, 'סך עלות דיור מוגן בערך נוכחי'),
            (deal1_name, 'ממוצע עלות לחודש בערך נוכחי'),
        ])
        columns_limited_details = [
            ('', 'שנה'),
            (deal0_name, 'סך עלות דיור מוגן בערך נוכחי'),
            (deal0_name, 'ממוצע עלות לחודש בערך נוכחי'),
            (deal1_name, 'סך עלות דיור מוגן בערך נוכחי'),
            (deal1_name, 'ממוצע עלות לחודש בערך נוכחי'),
        ]
    else:
        columns = pd.MultiIndex.from_tuples([
            ('', 'שנה'),
            (deal0_name, 'פיקדון שיוחזר'),
            (deal0_name, 'ערך נוכחי של פיקדון שיוחזר'),
            (deal0_name, 'ערך נוכחי של תשלומים חודשיים'),
            (deal0_name, 'סך עלות דיור מוגן בערך נוכחי'),
            (deal0_name, 'ממוצע עלות לחודש בערך נוכחי'),
        ])
        columns_limited_details = [
            ('', 'שנה'),
            (deal0_name, 'סך עלות דיור מוגן בערך נוכחי'),
            (deal0_name, 'ממוצע עלות לחודש בערך נוכחי'),
        ]

    # Create DataFrame
    df = pd.DataFrame(combined_rows, columns=columns)

    # Display RTL table
    if show_details:
        # Full details
        if second_offer_exists:
            tab_html = df.style.apply(highlight_lowest, axis=1).format("{:,}").hide(axis="index").to_html()
        else:
            tab_html = df.style.format("{:,}").hide(axis="index").to_html()
    else:
        # Limited details
        df_subset = df[columns_limited_details]
        if second_offer_exists:
            tab_html = df_subset.style.apply(highlight_lowest, axis=1).format("{:,}").hide(axis="index").to_html()
        else:
            tab_html = df_subset.style.format("{:,}").hide(axis="index").to_html()


    # rtl_html = f"""
    # <div dir="rtl" style="text-align: right">
    # {html}
    # </div>
    # """

    rtl_html = f"""<div dir="rtl" style="text-align: right"> {tab_html} </div>"""
    print(repr(tab_html))
    st.markdown(rtl_html, unsafe_allow_html=True)

rtl_html_explain = f"""
<div dir="rtl" style="text-align: right">
המחשבון עוזר להבין את המשמעות ארוכת השנים של הצעות שקיבלתם לדיור מוגן. תוכלו גם להשוות הצעות בין מקומות או להשוות בין אלטרנטיבות שהציעו לכם באותו דיור מוגן (הצעה בשיטת "דמי כניסה" לעומת הצעה ב"פיקדון").
<BR>
ריבית - הזינו ריבית שנתית שתשמש לחישובים. כמה? אם אתם עומדים להפקיד בפיקדון בדיור המוגן כסף שיש לכם, כיתבו את הריבית השנתית שאתם חושבים שתוכלו להרוויח אם הכסף יהיה אצלכם כל השנים במקום בפיקדון (נניח 4%). אם אתם לוקחים הלוואה כדי לממן דמי כניסה או פיקדון - אז הריבית השנתית של ההלוואה.
<BR>
המחשבון יציג מה תהיה העלות הכלכלית המצטברת אם תתגוררו בדיור המוגן שנה אחת, שנתיים, שלוש שנים וכו'. כל ההשוואות משתמשות בשיטה הכלכלית שנקראת "ערך נוכחי". השיטה נותנת ביטוי לכך שכסף שמשלמים בעתיד, שווה פחות מכסף שמשלמים כיום. לדוגמה אם הריבית היא 4%, אז לשלם היום 100 ש"ח זה כמו לשלם 104 ש"ח בעוד שנה. זה מאפשר לנו להשוות כלכלית, לדוגמה, בין הצעת פיקדון, שמתאפיינת בכך שמפקידים סכום גבוה בכניסה, לבין הצעה בתשלום חודשי בלבד, שמתאפיינת בתשלום חודשי גבוה יותר.
<BR>
גם לקבל כסף בעתיד, לדוגמה בהחזר פיקדון, שווה כמובן פחות מלקבל כסף היום. הנה דוגמה איך זה משפיע עלינו כאן: נניח לדוגמה שבכניסה תפקידו 1 מיליון ש"ח דמי פיקדון שישחקו מידי שנה ב- 4%. אם תצאו אחרי 5 שנים, תקבלו אז בחזרה 800 אלף ש"ח. בשיטת "ערך נוכחי", אנחנו מבינים שאם הריבית היא 4%, אז לקבל 800 אלף ₪ בעוד חמש שנים זה כמו לקבל היום רק 657,542 ₪. ולכן העלות הכלכלית של הפיקדון בשהייה במשך חמש שנים בדיור המוגן תהיה בערך נוכחי 342,458 אלף ₪ (מיליון שהפקדתם בכניסה פחות 657,542 ₪).
<BR>
דרך אגב, שימו לב שכאשר המחשבון מציג, לדוגמה, ששנתיים של מגורים יעלו בסה"כ 300 אלף ש"ח בערך נוכחי, הכוונה היא שזו העלות בהנחה שאחרי שנתיים יוצאים מהדיור המוגן. כי המחשבון לוקח בחשבון את החזר הפיקדון שיתקבל אחרי שנתיים, והחזר של פיקדון מקבלים כמובן רק אם יוצאים מהדיור המוגן.
</div>
"""

with st.expander("הסברים שחשוב לקרוא!"):
    st.markdown(rtl_html_explain, unsafe_allow_html=True)


rtl_html_TOU = f"""
<div dir="rtl" style="text-align: right">
אנחנו לא כלכלנים ולא מומחים לדיור מוגן, אז "אין אחריות" על הדיוק. אם זיהיתם טעות, תגידו. ובכלל, אם יש לכם שאלות או פידבק, נשמח מאוד אם תכתבו לנו!
<BR>
amirvang@gmail.com
</div>
"""

with st.expander("אודות ותנאי שימוש"):
    st.markdown(rtl_html_TOU, unsafe_allow_html=True)