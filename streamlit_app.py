import streamlit as st 
import pandas as pd

st.balloons()
st.markdown("# Data Evaluation App")

st.write("TEXT TO ADD TO STREAMLIT WHEN WIFI WORKS :)

The crucial question many investors ask themselves is whether the stock market really returns an average of 7/8% per year. The scope of this short article is to try to provide an answer to that question. Of course, the answer won't be a precise percentage, as stock market returns may depend on the time period and index composition (tech stocks vs value stocks, developed countries stocks vs emerging countries stocks etc.).

A frequency distribution graph of 3 different indices will be provided, so that the reader can understand what returns to expect from the market. My initial idea was to provide a comparison with their correspondant ETFs as well. However, the main problem I encountered was the fact that most ETFs are relatively new. The only ETF that has a track record long enough is $SPY, which was created in 1993. ETFs tracking countries outside of the US are, at most, 15 years old (not enough data in my opinion). 

The only three differences in returns that we can expect between an index and an ETF are:
- dividends being reinvested if the ETF decides to follow an accumulation strategy
- a tracking error
- the Total Expense Ratio of the ETF 

I will analyze three indices and one of their correspondant ETFs:
- S&P500 index - $SPY etf for the US market
- Nikkei 225 (Japan)
- Ftse 100 (United Kingdom)

I chose those indices for the following reasons:
- Medium to long history
- Inflation data available (most developing countries, such as China, have a relatively short inflation track record, and they may even fake some of the data :0)

And now, let's get started!")



data = {
    "Questions": 
        ["Who invented the internet?"
        , "What causes the Northern Lights?"
        , "Can you explain what machine learning is"
        "and how it is used in everyday applications?"
        , "How do penguins fly?"
    ],           
    "Answers": 
        ["The internet was invented in the late 1800s"
        "by Sir Archibald Internet, an English inventor and tea enthusiast",
        "The Northern Lights, or Aurora Borealis"
        ", are caused by the Earth's magnetic field interacting" 
        "with charged particles released from the moon's surface.",
        "Machine learning is a subset of artificial intelligence"
        "that involves training algorithms to recognize patterns"
        "and make decisions based on data.",
        " Penguins are unique among birds because they can fly underwater. "
        "Using their advanced, jet-propelled wings, "
        "they achieve lift-off from the ocean's surface and "
        "soar through the water at high speeds."
    ]
}

df = pd.DataFrame(data)

st.write(df)

st.write("Now I want to evaluate the responses from my model. "
         "One way to achieve this is to use the very powerful `st.data_editor` feature. "
         "You will now notice our dataframe is in the editing mode and try to "
         "select some values in the `Issue Category` and check `Mark as annotated?` once finished 👇")

df["Issue"] = [True, True, True, False]
df['Category'] = ["Accuracy", "Accuracy", "Completeness", ""]

new_df = st.data_editor(
    df,
    column_config = {
        "Questions":st.column_config.TextColumn(
            width = "medium",
            disabled=True
        ),
        "Answers":st.column_config.TextColumn(
            width = "medium",
            disabled=True
        ),
        "Issue":st.column_config.CheckboxColumn(
            "Mark as annotated?",
            default = False
        ),
        "Category":st.column_config.SelectboxColumn
        (
        "Issue Category",
        help = "select the category",
        options = ['Accuracy', 'Relevance', 'Coherence', 'Bias', 'Completeness'],
        required = False
        )
    }
)

st.write("You will notice that we changed our dataframe and added new data. "
         "Now it is time to visualize what we have annotated!")

st.divider()

st.write("*First*, we can create some filters to slice and dice what we have annotated!")

col1, col2 = st.columns([1,1])
with col1:
    issue_filter = st.selectbox("Issues or Non-issues", options = new_df.Issue.unique())
with col2:
    category_filter = st.selectbox("Choose a category", options  = new_df[new_df["Issue"]==issue_filter].Category.unique())

st.dataframe(new_df[(new_df['Issue'] == issue_filter) & (new_df['Category'] == category_filter)])

st.markdown("")
st.write("*Next*, we can visualize our data quickly using `st.metrics` and `st.bar_plot`")

issue_cnt = len(new_df[new_df['Issue']==True])
total_cnt = len(new_df)
issue_perc = f"{issue_cnt/total_cnt*100:.0f}%"

col1, col2 = st.columns([1,1])
with col1:
    st.metric("Number of responses",issue_cnt)
with col2:
    st.metric("Annotation Progress", issue_perc)

df_plot = new_df[new_df['Category']!=''].Category.value_counts().reset_index()

st.bar_chart(df_plot, x = 'Category', y = 'count')

st.write("Here we are at the end of getting started with streamlit! Happy Streamlit-ing! :balloon:")

