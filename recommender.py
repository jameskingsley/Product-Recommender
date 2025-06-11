import streamlit as st
import pandas as pd

@st.cache_data
def load_rules(path='association_rules.csv'):
    df = pd.read_csv(path)
    #Converting string repr to sets
    df['antecedents'] = df['antecedents'].apply(eval).apply(set)
    df['consequents'] = df['consequents'].apply(eval).apply(set)
    return df

rules = load_rules()

st.title("Product Recommendation System from Association Rules")

#Extracting unique products from antecedents
unique_products = set()
for antecedent in rules['antecedents']:
    unique_products.update(antecedent)
unique_products = sorted(unique_products)

selected_products = st.multiselect(
    "Select products the customer has purchased:",
    options=unique_products
)

min_conf = st.slider("Minimum Confidence", 0.0, 1.0, 0.6, 0.05)
min_lift = st.slider("Minimum Lift", 0.0, 10.0, 1.0, 0.1)

if selected_products:
    def is_subset(antecedent_set, purchased_list):
        return antecedent_set.issubset(set(purchased_list))

    filtered_rules = rules[
        rules['antecedents'].apply(lambda x: is_subset(x, selected_products)) &
        (rules['confidence'] >= min_conf) &
        (rules['lift'] >= min_lift)
    ].sort_values(by='confidence', ascending=False)

    if filtered_rules.empty:
        st.warning("No matching recommendations found with the current filters.")
    else:
        st.subheader("Recommended Products Based on Your Selection:")
        for idx, row in filtered_rules.iterrows():
            ant_str = ', '.join(row['antecedents'])
            cons_str = ', '.join(row['consequents'])
            st.markdown(f"**If customer buys:** {ant_str}")
            st.markdown(f"**Recommend:** {cons_str}")
            st.markdown(f"- Confidence: {row['confidence']:.2f}")
            st.markdown(f"- Lift: {row['lift']:.2f}")
            st.markdown(f"- Support: {row['support']:.4f}")
            st.markdown(f"- Leverage: {row['leverage']:.4f}")
            st.markdown("---")
else:
    st.info("Select at least one product from the list to get recommendations.")
