# Exploration of Propsper Loan data
## by Michael Smales
## August 2022


## Dataset

* The dataset contains over 100k loan listings from 2005 to 2014
* Each listing has a primary listing key, and contains foreign keys for the associated member (borrower) and the loan ID
* The data has 81 columns representing data for each listing including:
  - basic information about the listing (create dates etc)
  - the loan including amount, term, status, rate, loan purpose 
  - various risk scores 
  - borrower information such as occupation, state of residence, homeowner status, income range 
  - information from a credit report pull
  - information on the member's (borrower's) prior loans through Prosper 
  - information on payments on the loan associated with the listing
  - number of lenders already invested in the loan
* For this analysis, I filtered the dataset down to loans originated in 2012 only

## Summary of Findings

### Summary of univariate exploration
* Loan values range from \\$2-25k, are right-skewed, and have spikes at multiples of \$5k
* Below \\$5k, loan values tend to cluster around multiples of \$500
* Almost all loans in the dataset are fully-funded
* The most common loan duration is 36 months, followed by 60 months.  12 months is less common
* The reason for almost 50% of loans is debt consolidation.  After that household expenses, business and home improvements and other each get around 10% (by number of loans)
* Borrower APR ranges from 6% to 36%.  There is right skew, with a major peak at 36% APR loans
* Interestingly the risk rating is not as severely right-skewed.  It is bimodal, with peaks at 'C' (the middle of the range) and at 'HR', the high-risk loans

### Summary of bivariate exploration

**Investigation of rate**

* There is a high concentration of loans with values of <$5k and rates of 33-36%.  The remainder of loans are more evenly distributed, typically with values from $5-15k, and rates from 15%-30%
* As the loan becomes riskier (i.e. moving from category 'AA' to 'HR') two things happen
    1. The median rate increases from ~10% to ~36%
    2. Median loan value decreases. There appear to be value caps of $15k and $4k kicking in at risk categories 'D' and 'HR' respectively

**Investigation of loan reason**

* 3 categories, debt consolidation (DC), home improvements (HI) and business (B) have higher median loan sizes, lower median borrower rates, and a higher proportion of loans with good risk ratings, when compared to the other (O) and household expense (HE) categories

### Summary of multivariate exploration

* There is clear banding of the risk rating:
  - As the loan becomes riskier, the APR increases.  Visually there are well-defined limits for the APR for a given risk rating
  - Similarly, as the loan becomes riskier, the max value is capped.  These value caps come in and become more restrictive at each of ratings D, E and HR

## Key Insights for Presentation

* Loan values range from \\$4-25k with right skew, and spikes around $5k multiples
* Loan APRs range from 6% to 36%, with a spike in the number of loans at the 33-36% level
* As loans become riskier, APRs increase the loan value cap is reduced from \\$25k to $4k
* 27% of Prosper's loan portfolio is highly concentrated on small, high-APR loans (i.e. <$5k loans with 33-36% APR)  
* The top 5 reason categories account for 80% of Prosper's loans, with 'debt consolidation' alone accounting for ~50%
* Surprisingly, the debt consolidation category has the best loan risk profile among the top 5 categories 