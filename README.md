# Problem definition
The Coconut Craftworks, Co. manufactures a set of various products P. The company has selected
a set of their customers C to participate in a survey about its products. Since the company keeps
track on the past orders made by customers they know for each customer ci ∈ C what subset of
products Pi ⊆ P customers bought in the past.
Each customer ci ∈ C has expressed the interest to review at least li products (to get a discount
for future purchases) but at most ui of them (to not to get overloaded ). The marketing head of
The Coconut Craftworks, Co. requires to obtain at least vj reviews for each product j ∈ P in
order to have a good estimate of how much the products are likable by customers.<br />
Your tasks is to design a survey — distribute product surveys among customers, such that
* each customer is reviewing products that he/she knows;
* each customer gives at most one review per product;
* the total number of reviews each customer i provides lies in interval [li, ui];
* each product j is reviewed by at least vj customers;
* the total number of reviews is maximized

