# Build a pre-built subscription page with Stripe Checkout

# Prebuilt subscription page with Stripe Checkout 

Get started with our sample app to run a full, working subscription integration using [Stripe Billing](https://docs.stripe.com/billing.md) and [Stripe Checkout](https://docs.stripe.com/payments/checkout.md).

The sample app demonstrates redirecting your customers from your site to a prebuilt payment page hosted on Stripe. The Stripe Billing APIs create and manage subscriptions, invoices, and recurring payments, while Checkout provides the prebuilt, secure, Stripe-hosted UI for collecting payment details.

Click each step to see the corresponding sample code. As you interact with the steps, such as adding pricing data, the builder updates the sample code.

Download and customize the sample app locally to test your integration.

### Add your products and prices

Create new *Products* (Products represent what your business sells—whether that's a good or a service) and *Prices* (Prices define how much and how often to charge for products. This includes how much the product costs, what currency to use, and the interval if the price is for subscriptions) that you can use in this sample.

> Sign in to your Stripe account to configure your products and prices.

### Add features to your product

Create features, such as an annual birthday gift, and associate them with your subscription to [entitle](https://docs.stripe.com/billing/entitlements.md) new subscribers to them. Listen to the [active entitlements summary events](https://docs.stripe.com/billing/entitlements.md#webhooks) for your [event destination](https://docs.stripe.com/event-destinations.md), and use the [list active entitlements API](https://docs.stripe.com/api/entitlements/active-entitlement/list.md) for a given customer to fulfill your customer’s entitlements.

### (Optional) Enable payment methods

Use your [Dashboard](https://dashboard.stripe.com/settings/payment_methods) to enable [supported payment methods](https://docs.stripe.com/payments/payment-methods/payment-method-support.md) that you want to accept in addition to cards. Checkout dynamically displays your enabled payment methods in order of relevance, based on the customer’s location and other characteristics.

### Add a pricing preview page

Add a page to your site that displays your product and allows your customers to subscribe to it. Clicking **Checkout**, redirects them to a Stripe-hosted [Checkout](https://docs.stripe.com/payments/checkout.md) page, which finalizes the order and prevents further modification.

Consider embedding a [pricing table](https://docs.stripe.com/payments/checkout/pricing-table.md) to dynamically display your pricing information through the Dashboard. Clicking a pricing option redirects your customer to the payment page.

### Add a checkout button

The button on your order preview page redirects your customer to the Stripe-hosted payment page and uses your product’s `lookup_key` to retrieve the `price_id` from the server.

### Add a success page

Create a success page to display order confirmation messaging or order details to your customer. Associate this page with the Checkout Session `success_url`, which Stripe redirects to after the customer successfully completes the checkout.

### Add a customer portal button

Add a button to redirect to the customer portal to allow customers to manage their subscription. Clicking this button redirects your customer to the Stripe-hosted customer portal page.

### Redirect to the customer portal session

Make a request to the endpoint on your server to redirect to a new customer portal session. This example uses the `session_id` from the [Checkout session](https://docs.stripe.com/api/checkout/sessions/object.md#checkout_session_object-id) to demonstrate retrieving the `customer_id`. In a production environment, we recommend that you store this value alongside the authenticated user in your database.

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

The [Checkout Session](https://docs.stripe.com/api/checkout/sessions.md) controls what your customer sees in the Stripe-hosted payment page such as line items, the order amount and currency, and acceptable payment methods.

### Get the price from lookup key

Pass the lookup key you defined for your product in the [Price](https://docs.stripe.com/api/prices/list.md) endpoint to apply its price to the order.

### Define the line items

Always keep sensitive information about your product inventory, such as price and availability, on your server to prevent customer manipulation from the client. Pass in the predefined price ID retrieved above.

### Set the mode

Set the mode to `subscription`. Checkout also supports [payment](https://docs.stripe.com/checkout/quickstart.md) and [setup](https://docs.stripe.com/payments/save-and-reuse.md) modes for non-recurring payments.

### Supply success URL

Specify a publicly accessible URL that Stripe can redirect customers after success. Add the `session_id` query parameter at the end of your URL so you can retrieve the customer later and so Stripe can generate the customer’s hosted Dashboard.

### Redirect from Checkout

After creating the session, redirect your customer to the URL returned in the response (either the success or cancel URL).

### Create a customer portal session

Initiate a secure, Stripe-hosted [customer portal session](https://docs.stripe.com/api/customer_portal/sessions/create.md) that lets your customers manage their subscriptions and billing details.

### Redirect to customer portal

After creating the portal session, redirect your customer to the URL returned in the response.

### Fulfill the subscription

Create a `/webhook` endpoint and obtain your webhook secret key in the [Webhooks](https://dashboard.stripe.com/webhooks) tab in Workbench to listen for events related to subscription activity. After a successful payment and redirect to the success page, verify that the subscription status is `active` and grant your customer access to the products and features they subscribed to.

### Run the server

Start your server and go to [http://localhost:4242/](http://localhost:4242/)

```bash
npm start
```

### Run the server

Start your server. It automatically opens a browser window to [http://localhost:3000/checkout](http://localhost:3000/checkout)

```bash
npm start
```

### Run the server

Start your server and go to [http://localhost:4242/](http://localhost:4242/)

```bash
ruby server.rb
```

### Run the server

Start your server. It automatically opens a browser window to [http://localhost:3000/checkout](http://localhost:3000/checkout)

```bash
ruby server.rb
```

### Run the server

Start your server and go to [http://localhost:4242/](http://localhost:4242/)

```bash
python3 -m flask run --port=4242
```

### Run the server

Start your server. It automatically opens a browser window to [http://localhost:3000/checkout](http://localhost:3000/checkout)

```bash
python3 -m flask run --port=4242
```

### Run the server

Start your server and go to [http://localhost:4242/](http://localhost:4242/)

```bash
php -S 127.0.0.1:4242 --docroot=public
```

### Run the server

Start your server. It automatically opens a browser window to [http://localhost:3000/checkout](http://localhost:3000/checkout)

```bash
php -S 127.0.0.1:4242 --docroot=public
```

### Run the server

Start your server and go to [http://localhost:4242/](http://localhost:4242/)

```bash
dotnet run
```

### Run the server

Start your server. It automatically opens a browser window to [http://localhost:3000/checkout](http://localhost:3000/checkout)

```bash
dotnet run
```

### Run the server

Start your server and go to [http://localhost:4242/](http://localhost:4242/)

```bash
go run server.go
```

### Run the server

Start your server. It automatically opens a browser window to [http://localhost:3000/checkout](http://localhost:3000/checkout)

```bash
go run server.go
```

### Run the server

Start your server and go to [http://localhost:4242/](http://localhost:4242/)

```bash
java -cp target/sample-jar-with-dependencies.jar com.stripe.sample.Server
```

### Run the server

Start your server. It automatically opens a browser window to [http://localhost:3000/checkout](http://localhost:3000/checkout)

```bash
java -cp target/sample-jar-with-dependencies.jar com.stripe.sample.Server
```

### Try it out

Click the checkout button. In the Stripe-hosted payment page, use any of these test cards to simulate a payment.

| Scenario                        | Card Number      |
| ------------------------------- | ---------------- |
| Payment succeeds                | 4242424242424242 |
| Payment requires authentication | 4000002500003155 |
| Payment is declined             | 4000000000009995 |

## Add customization features

If you successfully subscribed to your product in your test, you have a working, basic subscriptions checkout integration. Use the toggles below to see how to customize this sample with additional features.

### Add trials

Attach a trial period to a Checkout session.

### Add a trial period

Use `subscription_data` to add an integer representing the number of `trial_period_days` before charging the customer for the first time. This must be at least `1`.

If you start a free trial without a payment method, set the `trial_settings[end_behavior][missing_payment_method]` field to `pause` or `cancel` so the subscription doesn’t continue if the trial ends with no payment method. Pass this parameter into `subscription_data` when you create a Checkout session, or update it on the subscription at another time. See [Use trial periods](https://docs.stripe.com/billing/subscriptions/trials.md#create-free-trials-without-payment) for more information.

### Set billing cycle date

Specify a billing cycle anchor when creating a Checkout session.

### Anchor the subscription billing cycle

Use `subscription_data` to set a `billing_cycle_anchor` timestamp for a subscription’s next billing date. See [Setting the billing cycle date in Checkout](https://docs.stripe.com/payments/checkout/billing-cycle.md) for more information.

### Automate tax collection

Calculate and collect the right amount of tax on your Stripe transactions. Learn more about [Stripe Tax](https://docs.stripe.com/tax.md) and [how to add it to Checkout](https://docs.stripe.com/tax/checkout.md). [Activate Stripe Tax](https://dashboard.stripe.com/tax) in the Dashboard before integrating.

### Add the automatic tax parameter

Set the `automatic_tax` parameter to `enabled: true`.

    <script src="https://js.stripe.com/clover/stripe.js"></script>
      <div class="product">
        <svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="14px" height="16px" viewBox="0 0 14 16" version="1.1">
            <defs/>
            <g id="Flow" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                <g id="0-Default" transform="translate(-121.000000, -40.000000)" fill="#E184DF">
                    <path d="M127,50 L126,50 C123.238576,50 121,47.7614237 121,45 C121,42.2385763 123.238576,40 126,40 L135,40 L135,56 L133,56 L133,4

... (truncated for reference)