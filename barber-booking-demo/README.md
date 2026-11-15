# Corner Chair local booking test

This is a local-only prototype for a fictional barbershop. It has test accounts,
one example chair, 30-minute appointment slots, and simulated payment choices.
No actual booking, payment processing, refunds, or payment details are involved.
Use made-up usernames and passwords that you do not use anywhere else.

From this directory, install the dependency and start the app:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Open `http://127.0.0.1:5001/`. Test data is stored in the ignored `instance`
directory; restarting the app signs users out. Run tests with:

```powershell
python -m unittest discover -s tests -v
```

This prototype binds only to localhost and is not production-ready or suitable
for real customer data. A public deployment needs an appropriate hosting
environment, HTTPS, a managed authentication and payment solution, account
recovery, abuse protection, and an independently reviewed booking and refund
policy. GitHub Pages cannot run the Python server.
