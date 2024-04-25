from app.calculations import add, subtract, multiply, divide, BankAccount, InsufficientFunds
import pytest

@pytest.mark.parametrize("num1, num2, expected", [(3, 2, 5),
                                                   (6, 7, 13),
                                                   (8, 1, 9)])
def test_add(num1, num2, expected):
    assert add(num1, num2) == expected

def test_subtract():
    assert subtract(9, 4) == 5

def test_multiply():
    assert multiply(3, 4) == 12

def test_divide():
    assert divide(2, 2) == 1

@pytest.fixture
def bank_account():
    return BankAccount(50)

@pytest.fixture
def zero_bank_account():
    return BankAccount()

def test_set_bank_initial_account(bank_account):
    assert bank_account.balance == 50

def test_zero_bank_initial_account(zero_bank_account):
    assert zero_bank_account.balance == 0

def test_deposit_account(bank_account):
    bank_account.deposit(20)
    assert bank_account.balance == 70

def test_withdrawal_account(bank_account):
    bank_account = BankAccount(50)
    bank_account.withdraw(20)
    assert bank_account.balance == 30

def test_get_interest(bank_account):
    bank_account.collect_interest()
    assert round(bank_account.balance, 2) == 55


@pytest.mark.parametrize("deposited, withdrew, expected", [(50, 10, 40),
                                                   (200, 7, 193),
                                                   (700, 5, 695)])
def test_bank_transactions(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected

def test_insuffisient_funds_on_account(zero_bank_account):
    with pytest.raises(InsufficientFunds):
        zero_bank_account.withdraw(200)