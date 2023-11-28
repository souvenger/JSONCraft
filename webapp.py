import streamlit as st
from json_parser import is_valid_json, parser, tokenizer
import json
from faker import Faker

fake = Faker()


def generate_sample_json():
    # Generate a sample JSON using Faker library
    sample_data = {
        "name": str(fake.name()),
        "email": str(fake.email()),
        "address": {
            "city": str(fake.city()),
            "state": str(fake.state()),
            "zip_code": str(fake.zipcode()),
        },
        "phone_number": str(fake.phone_number()),
        "is_student": str(fake.boolean()),
        "grades": [str(fake.random_int(60, 100)) for _ in range(5)],
    }
    return json.dumps(sample_data, indent=2)


def validate_and_edit():
    st.title("JSON Validation and Editing")

    # Text area for user input
    json_input = st.text_area("Enter JSON:", "", height=200)

    # Button to validate JSON
    if st.button("Validate JSON"):
        try:
            if is_valid_json(json_input):
                st.success("Valid JSON!")

                # Parse and display the content
                tokens = tokenizer(json_input)
                parsed_content = parser(tokens)
                st.subheader("Parsed JSON:")
                st.json(parsed_content)

                # Button to go to the Query System page
                if st.button("Go to Query System"):
                    st.experimental_set_query_params(parsed_json=parsed_content)
                    st.experimental_rerun()

            else:
                st.error("Invalid JSON. Please check the input.")
        except Exception as e:
            st.error(f"Error: {e}. Please provide a valid JSON input.")

    # Button to generate sample JSON
    if st.button("Generate Sample JSON"):
        sample_json = generate_sample_json()
        st.text_area("Generated Sample JSON:", sample_json, height=200)


def query_system():
    st.title("JSON Query System")

    # Get the parsed JSON from the query parameter
    parsed_json = st.experimental_get_query_params().get("parsed_json", [None])[0]

    if parsed_json is not None:
        st.subheader("Parsed JSON:")
        st.json(parsed_json)

        # Add your query system logic here
        # You can allow users to construct and execute queries on the parsed JSON
    else:
        st.warning(
            "No valid JSON to query. Please validate and parse JSON on the first page."
        )


def main():
    page = st.sidebar.selectbox("Select Page", ["Validate and Edit", "Query System"])

    if page == "Validate and Edit":
        validate_and_edit()
    elif page == "Query System":
        query_system()


if __name__ == "__main__":
    main()
