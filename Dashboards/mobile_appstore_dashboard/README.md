# HR Analytics Dashboard

[Mobile AppStore Dashboard](https://public.tableau.com/views/MobileAppStoreDashboard/MobileAppStoreDashboard?:language=en-US&:display_count=n&:origin=viz_share_link)

## Description

This Tableau dashboard is designed to provide insights into app characteristics and their performance in the App Store.

## Goals

The primary goals of this dashboard are to:

1. Provide insights into app characteristics and their performance in the App Store.
2. Enable users to filter and explore apps based on various attributes.
3. Analyze user ratings, pricing, and content rating for different app genres.
4. Understand the relationship between the number of screenshots and the number of supported languages.
5. Explore licensing information and its impact on user ratings.

## Potential Audience

- App developers and publishers
- App store analysts and administrators
- Market researchers and app enthusiasts

## Key Features
1. **Overview:**
   - Summary view showing the total number of apps, average user ratings, and total downloads.

2. **App Genre Analysis:**
   - Bar chart showing the count of apps by primary genre.
   - Bar chart showing the average user rating by primary genre.
   - Bar chart showing the average price by primary genre.
   - Filters for primary genre.

3. **User Ratings:**
   - Scatter plot comparing "user_rating" and "rating_count_tot."
   - Bar chart showing the average user rating for the current version by content rating.
   - Bar chart showing the average user rating for all versions by content rating.

4. **Pricing Analysis:**
   - Box plot or histogram showing the distribution of app prices.
   - Bar chart showing the average price by primary genre.

5. **Screenshots and Supported Languages:**
   - Scatter plot comparing "ipadSc_urls.num" and "lang.num."
   
6. **Licensing Information:**
   - Pie chart showing the distribution of apps with and without VPP device-based licensing.
   - Bar chart showing the average user rating for apps with and without VPP licensing.

## Requirements

- [Tableau Public](https://www.tableau.com/products/public) for dashboard modification and exploration.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

## Acknowledgments

- This dashboard is a fictitious example created for educational purposes.
- Data source: [Mobile App Store Dataset](https://www.kaggle.com/datasets/ramamet4/app-store-apple-data-set-10k-apps)

