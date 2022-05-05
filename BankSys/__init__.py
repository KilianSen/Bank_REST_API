import copy
import os.path
from dataclasses import dataclass
from uuid import uuid4
import sqlite3


class LLBank:
    @dataclass
    class Transaktion:
        uuid: str

        origin: str
        destination: str

        value: float

        def toDict(self) -> {}:
            return {'uuid': self.uuid,
                    'origin': self.origin,
                    'destination': self.destination,
                    'value': self.value}

        def toList(self) -> []:
            return [x for _, x in self.toDict().items()]

    @dataclass
    class Account:
        uuid: str

        name: str

        transaction_ids: [int]

        CREDIT_POSSIBLE = False
        CREDIT_MAX = 1000

        def toDict(self) -> {}:
            return {'uuid': self.uuid,
                    'name': self.name,
                    'transaction_ids': ';'.join(self.transaction_ids),
                    'CREDIT_POSSIBLE': self.CREDIT_POSSIBLE,
                    'CREDIT_MAX': self.CREDIT_MAX}

        def toList(self) -> []:
            return [x for _, x in self.toDict().items()]

    accounts: {str: Account}
    transactions: {str: Transaktion}

    def save(self):
        con = None
        print(self.bank_name)
        con = sqlite3.connect(f'{self.bank_name}_data.db')

        con.execute("""DROP TABLE IF EXISTS Transactions""")
        con.execute("""DROP TABLE IF EXISTS Accounts""")

        con.commit()

        con.execute("""
                    CREATE TABLE IF NOT EXISTS Transactions (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        uuid TEXT,
                        origin TEXT,
                        destination TEXT,
                        value REAL
                    );
                """)
        con.execute("""
                    CREATE TABLE IF NOT EXISTS Accounts (
                        id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                        uuid TEXT,
                        name TEXT,
                        transaction_ids TEXT,
                        credit_possible BOOLEAN,
                        credit_max REAL
                    );
                """)

        con.commit()
        for i in self.transactions:
            con.execute(
                """INSERT INTO Transactions (uuid, origin, destination, value) VALUES (?,?,?,?)""",
                tuple(self.transactions[i].toList()))
            con.commit()
        for i in self.accounts:
            v = """INSERT INTO Accounts (uuid, name, transaction_ids, credit_possible, credit_max) VALUES (?,?,?,?,?)"""
            con.execute(v, tuple(self.accounts[i].toList()))
            con.commit()
        con.close()

    def load(self):
        con = sqlite3.connect(f'{self.bank_name}_data.db')

        l_accs: {str: object} = {}
        for i in con.execute("""SELECT * FROM Accounts""").fetchall():
            acc = self.Account(i[1], i[2], i[3].split(';'))
            acc.CREDIT_POSSIBLE = i[4]
            acc.CREDIT_MAX = i[5]
            l_accs[acc.uuid] = acc

        l_trans: {str: object} = {}
        for i in con.execute("""SELECT * FROM Transactions""").fetchall():
            trans = self.Transaktion(i[1], i[2], i[3], i[4])
            l_trans[trans.uuid] = trans

        con.close()
        self.accounts = l_accs
        self.transactions = l_trans

    @staticmethod
    def load_avaiable() -> bool:
        return os.path.exists('../bank_data.db')

    # def __del__(self):
    #     self.save()

    def __init__(self, name: str = 'bank'):
        self.bank_name = name

        self.accounts = {}
        self.transactions = {}
        if self.load_avaiable():
            self.load()
        else:
            self.create_account('0', [], start_balance=0, creditable=True, credit_value=-1, uuid_override="0")
            self.save()

    def create_transaction(self, origin: str, destination: str, value: float) -> str:
        tra = self.Transaktion(uuid4().__str__(), origin, destination, value)
        self.transactions[tra.uuid] = tra
        return tra.uuid

    def create_account(self, name: str, transactions: [int], start_balance: float = 0, creditable: bool = False,
                       credit_value: float = 1000, uuid_override: str = None) -> str:

        acc = self.Account(uuid4().__str__(), name, transactions)
        acc.CREDIT_POSSIBLE = creditable
        acc.CREDIT_MAX = credit_value

        if uuid_override is not None:
            acc.uuid = uuid_override

        if start_balance > 0:
            acc.transaction_ids.append(self.create_transaction("0", acc.uuid, start_balance))

        self.accounts[acc.uuid] = acc
        return acc.uuid

    def get_balance(self, uuid: str) -> float:
        f = self.accounts[uuid].transaction_ids
        val = 0
        for i in f:
            if i == '':
                continue
            trans = self.transactions[i]
            if trans.origin == uuid:
                val -= trans.value
            elif trans.destination == uuid:
                val += trans.value
        return val


class Bank:
    __llb: LLBank

    class Account(LLBank.Account):
        _cb: callable

        @property
        def balance(self):
            return self._cb(self.uuid)

        def __repr__(self):
            tmp_lst = []
            for i in list(f'{k}={v}' for k, v in self.__dict__.items()):
                if not i.startswith('_'):
                    tmp_lst.append(i)
            tmp_lst.append(f'balance={self.balance}')
            return str(self.__class__.__name__) + '(' + ', '.join(tmp_lst) + ')'

        def toDict(self) -> {}:
            return {'uuid': self.uuid,
                    'name': self.name,
                    'transaction_ids': ';'.join(self.transaction_ids),
                    'balance': self.balance,
                    'CREDIT_POSSIBLE': self.CREDIT_POSSIBLE,
                    'CREDIT_MAX': self.CREDIT_MAX}

    def __init__(self, bank_name: str = 'bank'):
        self.__llb = LLBank(bank_name)

    def __del__(self):
        self.__llb.save()

    # <editor-fold desc="Account get">

    @property
    def accounts(self) -> [str]:
        return (i for i in self.__llb.accounts)

    def account(self, uuid: str) -> Account:
        acc = copy.copy(self.__llb.accounts[uuid])
        acc2 = self.Account(acc.uuid, acc.name, acc.transaction_ids)
        acc2.CREDIT_MAX = acc.CREDIT_MAX
        acc2.CREDIT_POSSIBLE = acc.CREDIT_POSSIBLE
        acc2._cb = self.__llb.get_balance
        return acc2

    # </editor-fold>

    # <editor-fold desc="Transaction get">

    @property
    def transactions(self) -> [str]:
        return (i for i in self.__llb.transactions)

    def transaction(self, uuid: str) -> LLBank.Transaktion:
        return copy.copy(self.__llb.transactions[uuid])

    # </editor-fold>

    def account_create(self, name: str) -> str:
        return self.__llb.create_account(name=name, transactions=[], start_balance=0, creditable=True,
                                         credit_value=1000)

    def transaction_create(self, origin: str, destination: str, value: float):

        if origin not in self.__llb.accounts:
            return None

        origin_info = self.account(origin)
        if (self.__llb.get_balance(origin) + origin_info.CREDIT_MAX if origin_info.CREDIT_POSSIBLE else 0) < value:
            if origin_info.CREDIT_POSSIBLE and origin_info.CREDIT_MAX == -1:
                pass
            else:
                return None

        new_transaction_id = self.__llb.create_transaction(origin, destination, value)

        self.__llb.accounts[origin].transaction_ids.append(new_transaction_id)
        self.__llb.accounts[destination].transaction_ids.append(new_transaction_id)

        return new_transaction_id