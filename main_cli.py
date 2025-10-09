# Import only the required functions and constants from the module
from sobriety_calculator import (
    init,
    choose_language,
    input_date,
    calculate_sobriety_delta,
    format_output,
    MESSAGES,
    get_date
)
def main():
    """
    Main function to run the sobriety calculator CLI.
    Handles language selection, date input, calculation, and output formatting.
    """

    init()  # Initialize settings or configurations

    # Select language and input date
    lang = choose_language()
    given_date = get_date(lang)

    # Calculate total days and relative difference
    total_days, delta_relative = calculate_sobriety_delta(given_date)

    # Format and print the output
    output_days, output_relative = format_output(total_days, delta_relative, lang)
    print("-" * 40)
    print(output_days)
    print(output_relative)
    print("-" * 40)



if __name__ == "__main__":
    # Script entry point
    main()