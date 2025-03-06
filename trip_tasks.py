from crewai import Task
from textwrap import dedent
from datetime import date

class TripTasks:
    def identify_task(self, agent, origin, cities, interests, range):
        return Task(
            description=dedent(f"""
                Analyze and select the best city for the trip based 
                on specific criteria such as weather patterns, seasonal
                events, and travel costs. This task involves comparing
                multiple cities, considering factors like current weather
                conditions, upcoming cultural or seasonal events, and
                overall travel expenses. 
                
                Your final answer must be a detailed
                report on the chosen city, and everything you found out
                about it, including the actual flight costs, weather 
                forecast and attractions.
                {self.__tip_section()}

                Traveling from: {origin}
                City Options: {cities}
                Trip Date: {range}
                Traveler Interests: {interests}
            """),
            agent=agent,
            expected_output="Detailed report on the chosen city including flight costs, weather forecast, and attractions"
        )

    def gather_task(self, agent, origin, interests, range):
        return Task(
            description=dedent(f"""
                As a local expert on this city you must compile an 
                in-depth guide for someone traveling there and wanting 
                to have THE BEST trip ever!
                Gather information about key attractions, local customs,
                special events, and daily activity recommendations.
                Find the best spots to go to, the kind of place only a
                local would know.
                This guide should provide a thorough overview of what 
                the city has to offer, including hidden gems, cultural
                hotspots, must-visit landmarks, weather forecasts, and
                high level costs.
                
                The final answer must be a comprehensive city guide, 
                rich in cultural insights and practical tips, 
                tailored to enhance the travel experience.
                {self.__tip_section()}

                Trip Date: {range}
                Traveling from: {origin}
                Traveler Interests: {interests}
            """),
            agent=agent,
            expected_output="Comprehensive city guide including hidden gems, cultural hotspots, and practical travel tips"
        )

    def plan_task(self, agent, origin, interests, range):
        return Task(
         description=dedent(f"""
            Expand this guide into a full travel 
            itinerary based on the date range given by the user, 
            so if the date range is of ten days 
            then the trip itinerary is for ten days and if it is 
            for 7 days then itinerary is for seven days. Give result                        
            with detailed per-day plans, including 
            weather forecasts, places to eat, packing suggestions, 
            and a budget breakdown.
            I am also giving you the reference date input which will 
            come 03/11/2024 to 05/11/2024, this means it is from 3rd
            November till 5th November
            
            You MUST suggest actual places to visit, actual hotels 
            to stay, actual restaurants to go to, and optimal transportation 
            logistics (flights, trains, buses, or car rentals) from the origin 
            to the destination and within the city.
            
            This itinerary should cover all aspects of the trip, 
            from arrival to departure, integrating the city guide
            information with practical travel logistics.
            
            Your final answer MUST start with a brief overview of the whole trip and then
            be a complete expanded travel plan,formatted as a bullet point list, with each day shown in a different paragraph, 
            broken into as many paragraphs as possible, including anticipated weather conditions, 
            recommended clothing and items to pack, and a detailed budget. Be specific and give 
            reasons why you picked each place, what makes them special. Use '---' to separate days 
            and sections.
            
            After the daily itinerary, include a SEPARATE SECTION titled "Accommodation Options"
            that lists accommodations day by day with details including:
            - Hotel/accommodation name for each day of the trip
            - Brief description of the accommodation
            - Price range
            - Actual working URL for booking
            - Any special amenities or features
            Format each accommodation option as a bullet point with the URL in parentheses,
            like: "- Day 1: Hilton Garden Inn - Luxury hotel with pool, $150/night
            (https://www.booking.com/hotel/hilton-garden.html)".
            
            After that, include a separate section titled 
            "Logistics Options" that lists transportation suggestions (e.g., flights, trains, buses, car rentals) 
            from {origin} to the destination city, including estimated costs, travel times, reasons, 
            and clickable URLs for booking or more information. Format each logistics option as a bullet point 
            with the URL in parentheses, like: "- Flight: Fly from {origin} to destination, $200, 4 hours, 
            reason: speed (https://www.britishairways.com/en-us/destinations/dubai/flights-to-dubai)". 
            Use real, functional URLs for airlines (e.g., British Airways, Emirates), transportation services 
            (e.g., Dubai Metro, Careem), and hotel bookings (e.g., Expedia, Booking.com).
            
            Finally, include a comprehensive "Detailed Budget Breakdown" section that shows:
            1. Day-by-day expenses with itemized costs for each day:
               - Accommodation costs
               - Meal costs (breakfast, lunch, dinner)
               - Activity/attraction entrance fees
               - Local transportation costs
               - Miscellaneous expenses
            
            2. Category totals with calculations:
               - Total accommodation costs (with formula showing per night × number of nights)
               - Total meal costs (showing calculations for avg cost per meal × meals × days)
               - Total transportation costs (broken down by type: flights, local transit, etc.)
               - Total activity costs (sum of all entrance fees and paid activities)
               - Total miscellaneous expenses
            
            3. Overall trip budget with:
               - Subtotals for each category
               - Grand total with calculation
               - Per-person-per-day average cost
               - Suggested emergency/contingency fund (10-15% of total)
            
            Format the budget in a clear, easy-to-understand way with actual dollar amounts and 
            calculations shown. For example:
            "Accommodation: $150/night × 7 nights = $1,050"
            "Daily meals: $50/day × 7 days = $350"
            
            After the budget section, include a separate section titled "Real-Time Flight Pricing"
            that provides up-to-date flight options for the specified date range from {origin} to
            the destination. For each flight option include:
            - Airline name and flight number(s)
            - Departure and arrival times
            - Current price with currency
            - Travel duration
            - Number of stops (if any)
            - Class options (Economy, Premium Economy, Business, First) with price differences
            - Baggage allowance
            - Reliable booking URL (e.g., to the airline's official site or trusted booking platforms like Expedia, Kayak, or Skyscanner)
            Format each flight option as a bullet point with the URL in parentheses, for example:
            "- Emirates EK506: {origin} to Dubai, 9:15 AM - 7:45 PM, $750, 8h 30m, 0 stops, Economy (20kg baggage)
            (https://www.emirates.com/us/english/book/)"
            
            Next, include a section titled "Weather Forecast and Packing Suggestions" that provides:
            - Day-by-day weather forecast for the destination during the trip dates
            - Temperature ranges (high/low) in both Fahrenheit and Celsius
            - Precipitation probability and expected conditions
            - Detailed packing list based on the forecasted weather, planned activities, and local customs
            - Special items needed for specific activities or locations
            - Seasonal considerations and local weather patterns to be aware of
            
            Finally, include a section titled "Restaurant Reservations" that recommends:
            - At least one restaurant option for each day of the trip
            - Price range and cuisine type for each restaurant
            - Signature dishes or specialties to try
            - Reservation requirements (whether booking in advance is necessary)
            - Direct reservation links or phone numbers
            - Best times to visit and estimated wait times
            Format each restaurant recommendation as a bullet point with reservation details, for example:
            "- Day 2 Dinner: La Petite Maison - High-end French-Mediterranean cuisine, $$$, Signature dish: Burrata
            with tomatoes and basil. Reservations required 2-3 weeks in advance.
            (https://www.lpmlondon.co.uk/dubai/)"
            
            Separate each section from the others with '---'.

            {self.__tip_section()}

            Trip Date: {range}
            Traveling from: {origin}
            Traveler Interests: {interests}
        """),
        agent=agent,
        expected_output="Text-based travel plan with daily schedules, accommodation section, logistics options, a comprehensive budget breakdown with calculations, real-time flight pricing, weather suggestions, and restaurant reservations"
    )

    def __tip_section(self):
        return "If you do your BEST WORK, I'll tip you $100!"