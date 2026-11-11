# Milestone-3

## 1. API Comparison

In Milestone 2, the SoupReplacer class was mainly responsible for storing the original and replacement tag names, while BeautifulSoup handled the actual transformation in popTag().

In Milestone 3, the SoupReplacer class is responsible for performing transformations through its transform() method, while BeautifulSoup only determines when to invoke it. This separates the transformation logic from the parsing logic, reducing coupling between the two components and making the code easier to maintain and extend.


## 2.Recommendation

I would recommend the Milestone 3 API because it offers greater flexibility and ease of use. By providing default values for optional arguments, users only need to specify the transformers they want to use instead of supplying every argument.

Although the Milestone 3 API might seem more complex, my implementation maintains backward compatibility with Milestone 2, allowing users to continue using the original tag replacement interface.

However, one potential downside is that an incorrectly implemented xformer callback could cause unexpected behavior or errors, since it can directly modify a Tag object.

Overall, the Milestone 3 API supports different use cases while keeping transformation logic centralized in the SoupReplacer class, which can reduce maintenance costs.
