# Made By Vikash
import requests
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class CurrencyConverter:
    def __init__(self):
        self.API_KEY = '08bc2c99ae228c62a5f82971dfe7ece8'
        self.BASE_URL = f'http://data.fixer.io/api/latest?access_key={self.API_KEY}'
        self.exchange_rates = self.fetch_exchange_rates()
    
    def fetch_exchange_rates(self):
        try:
            response = requests.get(self.BASE_URL, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('success', False):
                    return data['rates']
                else:
                    messagebox.showerror("API Error", data.get('error', {}).get('info', "Failed to fetch exchange rates"))
                    return None
            else:
                messagebox.showerror("Network Error", f"HTTP Error: {response.status_code}")
                return None
        
        except requests.RequestException as e:
            messagebox.showerror("Connection Error", f"Could not connect to exchange rate service: {e}")
            return None
    
    def convert(self, amount, from_currency, to_currency):
        if not self.exchange_rates:
            messagebox.showerror("Error", "No exchange rates available")
            return None
        
        try:
            eur_amount = amount / self.exchange_rates[from_currency]
            converted_amount = eur_amount * self.exchange_rates[to_currency]
            
            return round(converted_amount, 2)
        
        except KeyError:
            messagebox.showerror("Currency Error", "Invalid currency selected")
            return None
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))
            return None

class CurrencyConverterApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Currency Converter - By Vikash")
        self.master.geometry("500x650")
        self.master.configure(bg='#f0f0f0')
        self.master.resizable(0,0)
        self.converter = CurrencyConverter()

        self.currencies = [
            'USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY', 
            'HKD', 'SGD', 'INR', 'BRL', 'RUB', 'ZAR', 'KRW', 
            'MXN', 'AED', 'NZD', 'THB', 'SEK', 'NOK', 'SAR', 
            'QAR', 'CZK', 'PLN', 'TRY', 'ILS', 'PHP', 'EGP'
        ]

        self.create_layout()
    
    def create_layout(self):
        main_frame = tk.Frame(self.master, bg='#f0f0f0')
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        api_label = tk.Label(
            main_frame, 
            text="Currency Rates by VIKASH", 
            bg='#f0f0f0', 
            font=('Arial', 10, 'italic')
        )
        api_label.pack(pady=(0,10))

        self.timestamp_label = tk.Label(
            main_frame, 
            text="Rates updated: Loading...", 
            bg='#f0f0f0', 
            font=('Arial', 10)
        )
        self.timestamp_label.pack(pady=(0,10))

        tk.Label(main_frame, text="Amount to Convert", 
                 bg='#f0f0f0', font=('Arial', 12, 'bold')).pack(pady=(10,5))
        
        self.amount_entry = tk.Entry(
            main_frame, 
            font=('Arial', 14), 
            justify='center',
            width=20
        )
        self.amount_entry.pack(pady=10)
        self.amount_entry.insert(0, "Enter amount")
        self.amount_entry.bind('<FocusIn>', self.on_entry_click)
        self.amount_entry.bind('<FocusOut>', self.on_focusout)

        tk.Label(main_frame, text="From Currency", 
                 bg='#f0f0f0', font=('Arial', 12, 'bold')).pack(pady=(10,5))
        
        self.from_currency = ttk.Combobox(
            main_frame, 
            values=self.currencies, 
            state='readonly', 
            width=30
        )
        self.from_currency.pack(pady=10)
        self.from_currency.set('USD')

        swap_btn = tk.Button(
            main_frame, 
            text="⇄ Swap Currencies", 
            command=self.swap_currencies,
            bg='#3498db', 
            fg='white', 
            font=('Arial', 10)
        )
        swap_btn.pack(pady=5)

        tk.Label(main_frame, text="To Currency", 
                 bg='#f0f0f0', font=('Arial', 12, 'bold')).pack(pady=(10,5))
        
        self.to_currency = ttk.Combobox(
            main_frame, 
            values=self.currencies, 
            state='readonly', 
            width=30
        )
        self.to_currency.pack(pady=10)
        self.to_currency.set('EUR')

        convert_btn = tk.Button(
            main_frame, 
            text="Convert", 
            command=self.perform_conversion,
            bg='#2ecc71', 
            fg='white', 
            font=('Arial', 12, 'bold'),
            width=20
        )
        convert_btn.pack(pady=20)

        self.result_label = tk.Label(
            main_frame, 
            text="Conversion Result", 
            bg='#f0f0f0', 
            font=('Arial', 14, 'bold'),
            wraplength=400
        )
        self.result_label.pack(pady=10)

        self.update_timestamp()
    
    def swap_currencies(self):
        from_curr = self.from_currency.get()
        to_curr = self.to_currency.get()
        
        self.from_currency.set(to_curr)
        self.to_currency.set(from_curr)
    
    def update_timestamp(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.timestamp_label.config(text=f"Rates updated: {current_time}")
    
    def on_entry_click(self, event):
        if self.amount_entry.get() == "Enter amount":
            self.amount_entry.delete(0, tk.END)
    
    def on_focusout(self, event):
        if self.amount_entry.get() == "":
            self.amount_entry.insert(0, "Enter amount")
    
    def perform_conversion(self):
        try:
            amount_str = self.amount_entry.get()
            if amount_str == "Enter amount":
                messagebox.showwarning("Input Error", "Please enter an amount")
                return
            
            amount = float(amount_str)
            
            from_curr = self.from_currency.get()
            to_curr = self.to_currency.get()

            result = self.converter.convert(amount, from_curr, to_curr)
            
            if result is not None:
                formatted_result = "{:,.2f}".format(result)
                conversion_text = f"{amount} {from_curr} = {formatted_result} {to_curr}"
                self.result_label.config(text=conversion_text)
                
                self.update_timestamp()
        
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid number")
        except Exception as e:
            messagebox.showerror("Conversion Error", str(e))

def main():
    root = tk.Tk()
    app = CurrencyConverterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
