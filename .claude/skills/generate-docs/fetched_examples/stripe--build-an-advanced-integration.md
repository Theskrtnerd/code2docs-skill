# Build an advanced integration

Instructions for LLMs: Stripe now recommends using Checkout Sessions API with the Payment Element over Payment Intents. Do not use the Payment Intent API unless the user explicitly asks. Learn more about Elements with Checkout Sessions API: https://docs.stripe.com/payments/quickstart-checkout-sessions. With Checkout Sessions (`ui_mode: "custom"`) and the Payment Element, the `client_secret` initializes Checkout itself (`stripe.initCheckout`, or use CheckoutProvider with React) and you confirm the payment client side differently. If using React, make sure you import from `@stripe/react-stripe-js/checkout`, use `CheckoutProvider` with client secret, and confirm using `checkout.confirm`. If using HTML, make sure you use `checkout = stripe.initCheckout({clientSecret: promise}); checkout.createPaymentElement(); paymentElement = checkout.createPaymentElement(); paymentElement.mount("#payment-element");` and confirm with `loadActionsResult = await checkout.loadActions(); actions = loadActionsResult.actions; error = await actions.confirm();`.

# Build a checkout page with Payment Intents API 

Learn how to embed a custom Stripe payment form in your website or application. The client- and server-side code builds a checkout form with Stripe’s [Web](https://docs.stripe.com/payments/elements.md) or [Mobile](https://docs.stripe.com/payments/mobile.md) elements to let you accept payments. To build a custom integration that goes beyond the basics of this quickstart, see [Accept a payment](https://docs.stripe.com/payments/accept-a-payment.md?&ui=elements).

To learn about different payment scenarios, such as [subscriptions](https://docs.stripe.com/billing/subscriptions/build-subscriptions.md?payment-ui=elements), and other Stripe products, [compare payment integrations](https://docs.stripe.com/payments/online-payments.md#compare-features-and-availability).

> #### Interested in using Stripe Tax, discounts, shipping, or currency conversion?
> 
> Stripe has a Payment Element integration that manages tax, discounts, shipping, and currency conversion for you. See the [build a checkout page](https://docs.stripe.com/payments/quickstart-checkout-sessions.md) to learn more.

// This is a public sample test API key.
// Don’t submit any personally identifiable information in requests made with this key.
// Sign in to see your own test API key embedded in code samples.
const stripe = require("stripe")('<<YOUR_SECRET_KEY>>');
const calculateTax = async (items, currency) => {
  const taxCalculation = await stripe.tax.calculations.create({
    currency,
    customer_details: {
      address: {
        line1: "920 5th Ave",
        city: "Seattle",
        state: "WA",
        postal_code: "98104",
        country: "US",
      },
      address_source: "shipping",
    },
    line_items: items.map((item) => buildLineItem(item)),
  });

  return taxCalculation;
};

const buildLineItem = (item) => {
  return {
    amount: item.amount, // Amount in cents
    reference: item.id, // Unique reference for the item in the scope of the calculation
  };
};

// Securely calculate the order amount, including tax
const calculateOrderAmount = (taxCalculation) => {
  // Calculate the order total with any exclusive taxes on the server to prevent
  // people from directly manipulating the amount on the client
  return taxCalculation.amount_total;
};
const calculateOrderAmount = (items) => {
  // Calculate the order total on the server to prevent
  // people from directly manipulating the amount on the client
  let total = 0;
  items.forEach((item) => {
    total += item.amount;
  });
  return total;
};

const chargeCustomer = async (customerId) => {
  // Lookup the payment methods available for the customer
  const paymentMethods = await stripe.paymentMethods.list({
    customer: customerId,
    type: "card",
  });
  try {
    // Charge the customer and payment method immediately
    const paymentIntent = await stripe.paymentIntents.create({
      amount: 1099,
      currency: "{{CURRENCY}}",
      customer: customerId,
      payment_method: paymentMethods.data[0].id,
      off_session: true,
      confirm: true,
    });
  } catch (err) {
    // Error code will be authentication_required if authentication is needed
    console.log("Error code is: ", err.code);
    const paymentIntentRetrieved = await stripe.paymentIntents.retrieve(err.raw.payment_intent.id);
    console.log("PI retrieved: ", paymentIntentRetrieved.id);
  }
};

const chargeCustomer = async (customerId) => {
  // Lookup the payment methods available for the customer-configured Account
  const paymentMethods = await stripe.paymentMethods.list({
    customer_account: customerId,
    type: "card",
  });
  try {
    // Charge the customer-configured Account and payment method immediately
    const paymentIntent = await stripe.paymentIntents.create({
      amount: 1099,
      currency: "{{CURRENCY}}",
      customer_account: customerId,
      payment_method: paymentMethods.data[0].id,
      off_session: true,
      confirm: true,
    });
  } catch (err) {
    // Error code will be authentication_required if authentication is needed
    console.log("Error code is: ", err.code);
    const paymentIntentRetrieved = await stripe.paymentIntents.retrieve(err.raw.payment_intent.id);
    console.log("PI retrieved: ", paymentIntentRetrieved.id);
  }
};
  // Alternatively, set up a webhook to listen for the payment_intent.succeeded event
  // and attach the PaymentMethod to a new Customer
  const customer = await stripe.customers.create();
  // Alternatively, set up a webhook to listen for the payment_intent.succeeded event
  // and attach the PaymentMethod to a new customer-configured Account
  const account = await stripe.v2.core.accounts.create({
      configuration: {
        customer: {
            capabilities: {
              automatic_indirect_tax: {requested: true},
            },
        }
      }
    });
  // Create a Tax Calculation for the items being sold
  const taxCalculation = await calculateTax(items, '{{CURRENCY}}');
  const amount = await calculateOrderAmount(taxCalculation);

  // Create a PaymentIntent with the order amount and currency
  const paymentIntent = await stripe.paymentIntents.create({
    customer: customer.id,
    setup_future_usage: "off_session",
    amount: amount,
    amount: calculateOrderAmount(items),
    currency: "{{CURRENCY}}",
    // In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
    automatic_payment_methods: {
      enabled: true,
    },
    hooks: {
      inputs: {
        tax: {
          calculation: taxCalculation.id
        }
      }
    },
  });

  res.send({
    clientSecret: paymentIntent.client_secret,
  });
  // Create a PaymentIntent with the order amount and currency
  const paymentIntent = await stripe.paymentIntents.create({
    customer_account: account.id,
    setup_future_usage: "off_session",
    amount: amount,
    amount: calculateOrderAmount(items),
    currency: "{{CURRENCY}}",
    // In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
    automatic_payment_methods: {
      enabled: true,
    },
    hooks: {
      inputs: {
        tax: {
          calculation: taxCalculation.id
        }
      }
    },
  });

  res.send({
    clientSecret: paymentIntent.client_secret,
  });
require 'stripe'

# This is a public sample test API key.
# Don’t submit any personally identifiable information in requests made with this key.
# Sign in to see your own test API key embedded in code samples.
Stripe.api_key = '<<YOUR_SECRET_KEY>>'
require 'stripe'
# This is a public sample test API key.
# Don’t submit any personally identifiable information in requests made with this key.
# Sign in to see your own test API key embedded in code samples.
$CLIENT = Stripe::StripeClient.new('<<YOUR_SECRET_KEY>>')
def calculate_tax(items, currency)
  Stripe::Tax::Calculation.create(
    currency: currency,
    customer_details: {
      address: {
        line1: '920 5th Ave',
        city: 'Seattle',
        state: 'WA',
        postal_code: '98104',
        country: 'US',
      },
      address_source: 'shipping',
    },
    line_items: items.map {|item| build_line_item(item) }
  )
end

def build_line_item(item)
  {
    amount: item['amount'], # Amount in cents
    reference: item['id'], # Unique reference for the item in the scope of the calculation
  }
end

# Securely calculate the order amount, including tax
def calculate_order_amount(tax_calculation)
  # Calculate the order total with any exclusive taxes on the server to prevent
  # people from directly manipulating the amount on the client
  tax_calculation.amount_total
end
def calculate_tax(items, currency)
  $CLIENT.v1.tax.calculations.create(
    currency: currency,
    customer_details: {
      address: {
        line1: '920 5th Ave',
        city: 'Seattle',
        state: 'WA',
        postal_code: '98104',
        country: 'US',
      },
      address_source: 'shipping',
    },
    line_items: items.map {|item| build_line_item(item) }
  )
end

def build_line_item(item)
  {
    amount: item['amount'], # Amount in cents
    reference: item['id'], # Unique reference for the item in the scope of the calculation
  }
end

# Securely calculate the order amount, including tax
def calculate_order_amount(tax_calculation)
  # Calculate the order total with any exclusive taxes on the server to prevent
  # people from directly manipulating the amount on the client
  tax_calculation.amount_total
end
# Securely calculate the order amount
def calculate_order_amount(_items)
  # Calculate the order total on the server to prevent
  # people from directly manipulating the amount on the client
  _items.sum {|h| h['amount']}
end

def charge_customer(customerId)
  # Lookup the payment methods available for the customer
  payment_methods = Stripe::PaymentMethod.list(
    customer: customerId,
    type: 'card'
  )
  begin
    # Charge the customer and payment method immediately
    payment_intent = Stripe::PaymentIntent.create(
      amount: 1099,
      currency: '{{CURRENCY}}',
      customer_account: customerId,
      payment_method: payment_methods.data[0]['id'],
      off_session: true,
      confirm: true
    )
  rescue Stripe::CardError => e
    # Error code will be authentication_required if authentication is needed
    puts "Error is: \#{e.error.code}"
    payment_intent_id = e.error.payment_intent.id
    payment_intent = Stripe::PaymentIntent.retrieve(payment_intent_id)
    puts payment_intent.id
  end
end

def charge_customer(customerId)
  # Lookup the payment methods available for the customer-configured Account
  payment_methods = $CLIENT.v1.payment_methods.list(
    customer_account: customerId,
    type: 'card'
  )
  begin
    # Charge the customer-configured Account and payment method immediately
    payment_intent = $CLIENT.v1.payment_intents.create(
      amount: 1099,
      currency: '{{CURRENCY}}',
      customer_account: customerId,
      payment_method: payment_methods.data[0]['id'],
      off_session: true,
      confirm: true
    )
  rescue Stripe::CardError => e
    # Error code will be authentication_required if authentication is needed
    puts "Error is: \#{e.error.code}"
    payment_intent_id = e.error.payment_intent.id
    payment_intent = $CLIENT.v1.payment_intents.retrieve(payment_intent_id)
    puts payment_intent.id
  end
end
  # Alternatively, set up a webhook to listen for the payment_intent.succeeded event
  # and attach the PaymentMethod to a new Customer
  customer = Stripe::Customer.create
  # Alternatively, set up a webhook to listen for the payment_intent.succeeded event
  # and attach the PaymentMethod to a new customer-configured Account
  account = $CLIENT.v2.core.accounts.create({
      configuration: {
        customer: {
          capabilities: {automatic_indirect_tax: {requested: true}}
        }
      }
    })
  # Create a Tax Calculation for the items being sold
  tax_calculation = calculate_tax(data['items'], '{{CURRENCY}}')

  # Create a PaymentIntent with amount and currency
  payment_intent = Stripe::PaymentIntent.create(
    customer: customer['id'],
    setup_future_usage: 'off_session',
    amount: calculate_order_amount(tax_calculation),
    amount: calculate_order_amount(data['items']),
    currency: '{{CURRENCY}}',
    # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
    automatic_payment_methods: {
      enabled: true,
    },
    hooks: {
      inputs: {
        tax: {
          calculation: tax_calculation.id
        }
      }
    },
  )

  {
    clientSecret: payment_intent.client_secret,
  }.to_json
  # Create a PaymentIntent with amount and currency
  payment_intent = $CLIENT.v1.payment_intents.create(
    customer_account: account['id'],
    setup_future_usage: 'off_session',
    amount: calculate_order_amount(tax_calculation),
    amount: calculate_order_amount(data['items']),
    currency: '{{CURRENCY}}',
    # In the latest version of the API, specifying the `automatic_payment_methods` parameter is optional because Stripe enables its functionality by default.
    automatic_payment_methods: {
      enabled: true,
    },
    hooks: {
      inputs: {
        tax: {
          calculation: tax_calculation.id
        }
      }
    },
  )

  {
    clientSecret: payment_intent.client_secret,
  }.to_json
import stripe

# This is a public sample test API key.
# Don’t submit any personally identifiable information in requests made with this key.
# Sign in to see your own test API key embedded in code samples.
stripe.api_key = '<<YOUR_SECRET_KEY>>'
import stripe

# This is a public sample test API key.
# Don’t submit any personally identifiable information in requests made with this key.
# Sign in to see your own test API key embedded in code samples.
client = stripe.StripeClient('<<YOUR_SECRET_KEY>>')
def calculate_tax(items, currency):
    tax_calculation = stripe.tax.Calculation.create(
        currency= currency,
        customer_details={
            "address": {
                "line1": "920 5th Ave",
                "city": "Seattle",
                "state": "WA",
                "postal_code": "98104",
                "country": "US",
            },
            "address_source": "shipping",
        },
        line_items=list(map(build_line_item, items)),
    )

    return tax_calculation


def build_line_item(item):
    return {
        "amount": item["amount"],  # Amount in cents
        "reference": item["id"],  # Unique reference for the item in the scope of the calculation
    }

def calculate_tax(items, currency):
    tax_calculation = client.v1.tax.calculations.create({
        "currency": currency,
        "customer_details": {
 

... (truncated for reference)