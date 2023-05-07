from solana.rpc.api import Client
from spl.token.client import Token
from solana.transaction import Transaction
from solders.system_program import TransferParams, transfer
from solders.pubkey import Pubkey
from solders.signature import Signature
from solders.keypair import Keypair
from typing import Optional

class Solana_Simplified():
    def set_source_main_wallet_keypair(source_main_wallet_private_key: str):
        source_main_wallet_keypair = Keypair.from_base58_string(source_main_wallet_private_key)
        return source_main_wallet_keypair

    def set_main_wallet_publickey(main_wallet_address: str):
        main_wallet_public_key = Pubkey.from_string(main_wallet_address)
        return main_wallet_public_key

    def set_program_id_publickey(program_id: str):
        program_id_publickey = Pubkey.from_string(program_id)
        return program_id_publickey

    def set_token_address_publickey(token_address: str):
        token_address_publickey = Pubkey.from_string(token_address)
        return token_address_publickey

    def set_solana_client(development_url: Optional[str] = "https://api.mainnet-beta.solana.com"):
        solana_client = Client(development_url)
        return solana_client

    def set_spl_client(solana_client: Client, token_address_publickey: Pubkey, program_id_publickey: Pubkey, source_main_wallet_keypair: Keypair):
        spl_client = Token(conn=solana_client, pubkey=token_address_publickey, program_id=program_id_publickey, payer=source_main_wallet_keypair)
        return spl_client

    def get_token_wallet_address_from_main_wallet_address(spl_client: Token, main_wallet_address: Pubkey):
        try:
            token_wallet_address_public_key = spl_client.get_accounts_by_owner(owner=main_wallet_address, commitment=None, encoding='base64').value[0].pubkey
        except:
            token_wallet_address_public_key = spl_client.create_associated_token_account(owner=main_wallet_address, skip_confirmation=False, recent_blockhash=None)
        return token_wallet_address_public_key

    def verify_token_account(spl_client: Token, token_address_publickey: Pubkey):
        try:
            spl_client.get_account_info(account=token_address_publickey, commitment=None)
            return True
        except:
            print("Account not found")
            return False

    def get_main_wallet_solana_balance(solana_client: Client, sender_main_wallet_public_key: Pubkey):
        solana_balance = float(solana_client.get_balance(sender_main_wallet_public_key).value) / float(1000000000)
        return solana_balance

    def get_token_account_balance(spl_client: Token, token_address_publickey: Pubkey):
        token_balance = spl_client.get_balance(token_address_publickey).value.ui_amount_string
        return token_balance

    def approve_spl_token_transaction(spl_client: Token, source_token_address_publickey: Pubkey, delegate_token_address_publickey: Pubkey, owner_token_address_publickey: Pubkey, amount: float):
        amount = int(amount*1000000000)
        transaction_signature = spl_client.approve(source_token_address_publickey, delegate_token_address_publickey, owner_token_address_publickey, amount, multi_signers=None, opts=None, recent_blockhash=None).value
        return transaction_signature

    def send_spl_token(spl_client: Token, source_token_address_publickey: Pubkey, destination_token_address_publickey: Pubkey, source_main_wallet_keypair: Keypair, amount: float):
        transaction_signature = spl_client.transfer(source=source_token_address_publickey, dest=destination_token_address_publickey, owner=source_main_wallet_keypair, amount=int(float(amount)*1000000000), multi_signers=None, opts=None, recent_blockhash=None).value
        return str(transaction_signature)

    def send_solana(solana_client: Client, sender_main_wallet_public_key: Pubkey, destination_main_wallet_public_key: Pubkey, source_main_wallet_keypair: Keypair, amount: float):
        txn = Transaction().add(transfer(TransferParams(
            from_pubkey=sender_main_wallet_public_key, to_pubkey=destination_main_wallet_public_key, lamports=int(amount*1000000000))))
        transaction_signature = solana_client.send_transaction(txn, source_main_wallet_keypair).value
        return str(transaction_signature)

    def set_transaction_signature(transaction_signature_string: str):
        transaction_signature = Signature.from_string(transaction_signature_string)
        return transaction_signature

    def check_solana_transaction(solana_client: Client, transaction_signature: Signature):
        transaction_complete = solana_client.get_transaction(tx_sig=transaction_signature, encoding='json', commitment=None, max_supported_transaction_version=None)
        prior_balance = transaction_complete.value.transaction.meta.post_balances[0]
        initial_balance = transaction_complete.value.transaction.meta.pre_balances[0]
        if prior_balance == initial_balance:
            return False
        else:
            return True
        
    def check_approval_transaction(solana_client: Client, transaction_signature: Signature):
        transaction_complete = solana_client.get_transaction(tx_sig=transaction_signature, encoding='json', commitment=None, max_supported_transaction_version=None)
        return transaction_complete

    def check_token_transaction(solana_client: Client, transaction_signature: Signature):
        transaction_complete = solana_client.get_transaction(tx_sig=transaction_signature, encoding='json', commitment=None, max_supported_transaction_version=None)
        prior_balance = transaction_complete.value.transaction.meta.post_token_balances[0].ui_token_amount.ui_amount_string
        initial_balance = transaction_complete.value.transaction.meta.pre_token_balances[0].ui_token_amount.ui_amount_string
        if prior_balance == initial_balance:
            return False
        else:
            return True

    def check_solana_transaction_direct(solana_client: Client, transaction_signature: Signature):
        transaction_status = solana_client.confirm_transaction(tx_sig=transaction_signature, commitment=None, sleep_seconds=0.5, last_valid_block_height=None).value[0].confirmation_status
        return transaction_status
    
    def get_transaction_signature_list(solana_client: Client, owner_account: Pubkey):
        signatures = solana_client.get_signatures_for_address(owner_account, before=None, until=None, limit=None, commitment=None).value
        signatures_list = [signature.signature for signature in signatures]
        return signatures_list
    
    def get_transaction_details_from_signature(solana_client: Client, transaction_signature: Signature):
        transaction_complete = solana_client.get_transaction(tx_sig=transaction_signature, encoding='json', commitment=None, max_supported_transaction_version=0)
        return transaction_complete
    
    def check_transaction_status(solana_client: Client, sender_account: Pubkey, transaction_complete):
        try:
            prior_balance = transaction_complete.value.transaction.meta.post_token_balances[0].ui_token_amount.ui_amount_string
            initial_balance = transaction_complete.value.transaction.meta.pre_token_balances[0].ui_token_amount.ui_amount_string
            token_account = transaction_complete.value.transaction.transaction.message.account_keys[1]
            balance_change = abs(float(prior_balance) - float(initial_balance))
            balance_details = [balance_change, "token"]
            if prior_balance == initial_balance:
                return False
            else:
                if sender_account == token_account:
                    return balance_details
                else:
                    return False
        except:
            try:
                prior_balance = transaction_complete.value.transaction.meta.post_balances[0]
                initial_balance = transaction_complete.value.transaction.meta.pre_balances[0]
                solana_account = transaction_complete.value.transaction.transaction.message.account_keys[0]
                balance_change = abs(float(prior_balance) - float(initial_balance)) / float(1000000000)
                balance_details = [balance_change, "solana"]
                if prior_balance == initial_balance:
                    return False
                else:
                    if sender_account == solana_account:
                        return balance_details
                    else:
                        return False
            except:
                return False
