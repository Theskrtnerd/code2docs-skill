# Build a Stripe-hosted checkout page

# Stripe-hosted page 

Explore a full, working code sample of an integration with [Stripe Checkout](https://docs.stripe.com/payments/checkout.md) where customers click a button on your site and get redirected to a payment page hosted by Stripe. The example includes client- and server-side code, and the payment page is prebuilt.

### Install the Stripe Node library

Install the package and import it in your code. Alternatively, if you’re starting from scratch and need a package.json file, download the project files using the Download link in the code editor.

#### npm

Install the library:

```bash
npm install --save stripe
```

#### GitHub

Or download the stripe-node library source code directly [from GitHub](https://github.com/stripe/stripe-node).

### Install the Stripe Ruby library

Install the Stripe ruby gem and require it in your code. Alternatively, if you’re starting from scratch and need a Gemfile, download the project files using the link in the code editor.

#### Terminal

Install the gem:

```bash
gem install stripe
```

#### Bundler

Add this line to your Gemfile:

```bash
gem 'stripe'
```

#### GitHub

Or download the stripe-ruby gem source code directly [from GitHub](https://github.com/stripe/stripe-ruby).

### Install the Stripe Java library

Add the dependency to your build and import the library. Alternatively, if you’re starting from scratch and need a sample pom.xml file (for Maven), download the project files using the link in the code editor.

#### Maven

Add the following dependency to your POM and replace {VERSION} with the version number you want to use.

```bash
<dependency>\n<groupId>com.stripe</groupId>\n<artifactId>stripe-java</artifactId>\n<version>{VERSION}</version>\n</dependency>
```

#### Gradle

Add the dependency to your build.gradle file and replace {VERSION} with the version number you want to use.

```bash
implementation "com.stripe:stripe-java:{VERSION}"
```

#### GitHub

Download the JAR directly [from GitHub](https://github.com/stripe/stripe-java/releases/latest).

### Install the Stripe Python package

Install the Stripe package and import it in your code. Alternatively, if you’re starting from scratch and need a requirements.txt file, download the project files using the link in the code editor.

#### pip

Install the package through pip:

```bash
pip3 install stripe
```

#### GitHub

Download the stripe-python library source code directly [from GitHub](https://github.com/stripe/stripe-python/releases).

### Install the Stripe PHP library

Install the library with composer and initialize with your secret API key. Alternatively, if you’re starting from scratch and need a composer.json file, download the files using the link in the code editor.

#### Composer

Install the library:

```bash
composer require stripe/stripe-php
```

#### GitHub

Or download the stripe-php library source code directly [from GitHub](https://github.com/stripe/stripe-php).

### Set up your server

Add the dependency to your build and import the library. Alternatively, if you’re starting from scratch and need a go.mod file, download the project files using the link in the code editor.

#### Go

Make sure to initialize with Go Modules:

```bash
go get -u github.com/stripe/stripe-go/v84
```

#### GitHub

Or download the stripe-go module source code directly [from GitHub](https://github.com/stripe/stripe-go).

### Install the Stripe.net library

Install the package with .NET or NuGet. Alternatively, if you’re starting from scratch, download the files which contains a configured .csproj file.

#### dotnet

Install the library:

```bash
dotnet add package Stripe.net
```

#### NuGet

Install the library:

```bash
Install-Package Stripe.net
```

#### GitHub

Or download the Stripe.net library source code directly [from GitHub](https://github.com/stripe/stripe-dotnet).

### Install the Stripe libraries

Install the packages and import them in your code. Alternatively, if you’re starting from scratch and need a `package.json` file, download the project files using the link in the code editor.

Install the libraries:

```bash
npm install --save stripe @stripe/stripe-js next
```

### Create a Checkout Session

Add an endpoint on your server that creates a [Checkout Session](https://docs.stripe.com/api/checkout/sessions.md). A Checkout Session controls what your customer sees on the payment page such as line items, the order amount and currency, and acceptable payment methods. We enable cards and other common payment methods for you by default, and you can enable or disable payment methods directly in the [Stripe Dashboard](https://dashboard.stripe.com/settings/payment_methods).

### Create a Checkout Session

Add a [Route Handler](https://nextjs.org/docs/app/building-your-application/routing/route-handlers) in your application that creates a [Checkout Session](https://docs.stripe.com/api/checkout/sessions.md). A Checkout Session controls what your customer sees on the payment page such as line items, the order amount and currency, and acceptable payment methods. We enable cards and other common payment methods for you by default, and you can enable or disable payment methods directly in the [Stripe Dashboard](https://dashboard.stripe.com/settings/payment_methods).

### Define a product to sell

Always keep sensitive information about your product inventory, such as price and availability, on your server to prevent customer manipulation from the client. Define product information when you create the Checkout Session using [predefined price IDs](https://docs.stripe.com/payments/accept-a-payment.md?payment-ui=checkout&ui=stripe-hosted#create-product-prices-upfront) or on the fly with [price_data](https://docs.stripe.com/api/checkout/sessions/create.md#create_checkout_session-line_items-price_data).

### Choose a mode

To handle different transaction types, adjust the `mode` parameter. For one-time payments, use `payment`. To initiate recurring payments with [subscriptions](https://docs.stripe.com/billing/subscriptions/build-subscriptions.md?payment-ui=checkout&ui=stripe-hosted), switch the `mode` to `subscription`. And for [setting up future payments](https://docs.stripe.com/payments/save-and-reuse.md?platform=web&ui=stripe-hosted), set the `mode` to `setup`.

### Supply success URL

Specify a URL for the success page—make sure it’s publicly accessible so Stripe can redirect customers to it.

### Redirect to Checkout

After creating the session, redirect your customer to the URL for the Checkout page returned in the response.

### Add a success page

Create a success page for the URL you provided as the Checkout Session `success_url` to display order confirmation messaging or order details to your customer. Stripe redirects to this page after the customer successfully completes the checkout.

### Add an order preview page

Finally, add a page to show a preview of the customer’s order. Allow them to review or modify their order—as soon as they’re sent to the Checkout page, the order is final and they can’t modify it without creating a new Checkout Session.

### Add an order preview page

Add a page to show a preview of the customer’s order. Allow them to review or modify their order—as soon as they’re sent to the Checkout page, the order is final and they can’t modify it without creating a new Checkout Session.

### Add a checkout button

Add a button to your order preview page. When your customer clicks this button, they’re redirected to the Stripe-hosted payment page.

### Add a checkout button

Add a button to your order preview page. When your customer clicks this button, they’re redirected to the Stripe-hosted payment form.

### Add an order preview page

Add a file under `pages/` to create a page showing a preview of the customer’s order. Allow them to review or modify their order—as soon as they’re sent to the Checkout page, the order is final and they can’t modify it without creating a new Checkout Session

### Fetch a Checkout Session

Add a button to your order preview page. When your customer clicks it, make a request to the Route Handler to redirect the customer to a new Checkout Session.

### Handle redirect back from Checkout

Show a message to your customer when they’re redirected back to your page. Wait to fulfill orders (for example, shipping or sending email receipts) until the payment succeeds. Learn more about [fulfilling orders with Checkout](https://docs.stripe.com/checkout/fulfillment.md).

### Set your environment variables

Add your publishable and secret keys to a `.env` file. Next.js automatically loads them into your application as [environment variables](https://nextjs.org/docs/basic-features/environment-variables). If you want to listen to webhooks, also include a webhook secret, which you can create in the [Dashboard](https://dashboard.stripe.com/webhooks) or with the [Stripe CLI](https://docs.stripe.com/stripe-cli.md).

### Before you run the application

Add `“proxy”: “<http://localhost:4242>”` to your `package.json` file during local development.

### Run the application

Start your server and go to [http://localhost:4242/checkout.html](http://localhost:4242/checkout.html)

### Run the application

Start your server and go to [http://localhost:3000/checkout](http://localhost:3000/checkout)

### Run the application

Start your app with `npm run dev` and go to [http://localhost:3000](http://localhost:3000)

### Try it out

Click the checkout button to be redirected to the Stripe Checkout page. Use any of these test cards to simulate a payment.

| Scenario                        | Card Number      |
| ------------------------------- | ---------------- |
| Payment succeeds                | 4242424242424242 |
| Payment requires authentication | 4000002500003155 |
| Payment is declined             | 4000000000009995 |

## Congratulations!

You have a basic Checkout integration working. Now learn how to customize the appearance of your checkout page and automate tax collection.

### Customize the checkout page

Customize the appearance of the hosted Checkout page by:

- Adding your logo and color theme in your [branding settings](https://dashboard.stripe.com/settings/branding).
- Using the [Checkout Sessions API](https://docs.stripe.com/api/checkout/sessions/create.md) to activate additional features, like  collecting addresses or prefilling customer data.

### Prefill customer data

Use [customer_email](https://docs.stripe.com/api/checkout/sessions/create.md#create_checkout_session-customer_email) to prefill the customer’s email address in the email input field. You can also pass a [Customer](https://docs.stripe.com/api/customers.md) ID to the `customer` field to prefill the email address field with the email stored on the Customer.

### Pick a submit button

Configure the copy displayed on the Checkout submit button by setting the [submit_type](https://docs.stripe.com/api/checkout/sessions/create.md#create_checkout_session-submit_type). There are four different submit types.

### Collect billing and shipping details

Use [billing_address_collection](https://docs.stripe.com/api/checkout/sessions/create.md#create_checkout_session-billing_address_collection) and [shipping_address_collection](https://docs.stripe.com/api/checkout/sessions/create.md#create_checkout_session-shipping_address_collection) to collect your customer’s address. [shipping_address_collection](https://docs.stripe.com/api/checkout/sessions/create.md#create_checkout_session-shipping_address_collection) requires a list of `allowed_countries`. Checkout displays the list of allowed countries in a dropdown menu on the page.

### Preview the customized page

Click the checkout button to see a sample Stripe Checkout page with these additional fields. Learn more about all the ways you can [customize Checkout](https://docs.stripe.com/payments/checkout/customization.md).

### Automate tax collection

Calculate and collect the right amount of tax on your Stripe transactions. Learn more about [Stripe Tax](https://docs.stripe.com/tax.md) and how to [add it to Checkout](https://docs.stripe.com/tax/checkout.md).

### Set up Stripe Tax in the Dashboard

[Activate Stripe Tax](https://dashboard.stripe.com/tax) to monitor your tax obligations, automatically collect tax, and access the reports you need to file returns.

### Add the automatic tax parameter

Set the `automatic_tax` parameter to `enabled: true`.

### New and returning customers

By default, Checkout only creates [Customers](https://docs.stripe.com/api/customers.md) when one is required (for example, for subscriptions). Otherwise, Checkout uses [guest customers](https://docs.stripe.com/payments/checkout/guest-customers.md) to group payments in the Dashboard. You can optionally configure Checkout to always create a new customer or to specify a returning customer.

### Always create customers

To always create customers whenever one isn’t provided, set [customer_creation](https://docs.stripe.com/api/checkout/sessions/create.md#create_checkout_session-customer_creation) to `'always'`.

### Specify returning customers

To associate a Checkout Session with a customer that already exists, provide the [customer](https://docs.stripe.com/api/checkout/sessions/create.md#create_checkout_session-customer) when creating a session. If you model customers using Accounts v2, you can also pass an Account ID to the [customer_account](https://docs.stripe.com/api/checkout/sessions/create.md#create_checkout_session-customer_account) field to prefill the associated email address. Learn more about the [difference between using v1 Customers and v2 Accounts](https://docs.stripe.com/connect/use-accounts-as-customers.md).

// This test secret API key is a placeholder. Don't include personal details in requests with this key.
// To see your test secret API key embedded in code samples, sign in to your Stripe account.
// You can also find your test secret API key at https://dashboard.stripe.com/test/apikeys.
const stripe = require('stripe')('<<YOUR_SECRET_KEY>>');
  const session = await stripe.checkout.sessions.create({
    customer_email: 'customer@example.com',
    submit_type: 'donate',
    billing_address_collection: 'auto',
    shipping_address_collection: {
      allowed_countries: ['US', 'CA'],
    },
    line_items: [
      {
        // Provide the exact Price ID (for example, price_1234) of the product you want to sell
        price: '{{PRICE_ID}}',
        quantity: 1,
      },
    ],
    mode: {{CHECKOUT_MODE}},
    success_url: `${YOUR_DOMAIN}/success.html`,
    success_url: `${YOUR_DOMAIN}?success=true`,
    automatic_tax: {enabled: true},
    customer_creation: 'always',
    // Provide the Customer ID (for example, cus_1234) for an existing customer to associate it with this session
    // customer: '{{CUSTOMER_ID}}'
  });

  res.redirect(303, session.url);
{
  "name": "stripe-sample",
  "version": "1.0.0",
  "description": "A sample Stripe implem

... (truncated for reference)