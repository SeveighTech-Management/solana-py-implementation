from solana_simplified import Solana_Simplified
import time

#set all accounts
private_key = "<sender_account_private_key>"
main_wallet = "<sender_account_wallet_address>"
test_wallet = "<recipient_account_wallet_address>"
program_id = "<token_program_id>" #eg: https://solscan.io/token/FpekncBMe3Vsi1LMkh6zbNq8pdM6xEbNiFsJBRcPbMDQ | FpekncBMe3Vsi1LMkh6zbNq8pdM6xEbNiFsJBRcPbMDQ
mint = "<token_address>" #eg: https://solscan.io/account/TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA | TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA
source_main_wallet_keypair = Solana_Simplified.set_source_main_wallet_keypair(private_key)
sender_pubkey = Solana_Simplified.set_main_wallet_publickey(main_wallet)
destination_pubkey = Solana_Simplified.set_main_wallet_publickey(test_wallet)
program_pubkey = Solana_Simplified.set_program_id_publickey(program_id)
token_address_pubkey = Solana_Simplified.set_token_address_publickey(mint)

#set clients
solana_client = Solana_Simplified.set_solana_client()
spl_client = Solana_Simplified.set_spl_client(solana_client, token_address_pubkey, program_pubkey, source_main_wallet_keypair)

#set and check sender token account
sender_token_pubkey = Solana_Simplified.get_token_wallet_address_from_main_wallet_address(spl_client, sender_pubkey)
check_sender_token_account = Solana_Simplified.verify_token_account(spl_client, sender_token_pubkey)

#set and check destination token account
destination_token_pubkey = Solana_Simplified.get_token_wallet_address_from_main_wallet_address(spl_client, destination_pubkey)
check_destination_token_account = Solana_Simplified.verify_token_account(spl_client, destination_token_pubkey)

#get sender account balances
sender_solana_balance = Solana_Simplified.get_main_wallet_solana_balance(solana_client, sender_pubkey)
sender_token_balance = Solana_Simplified.get_token_account_balance(spl_client, sender_token_pubkey)

#get destination account balances
destination_solana_balance = Solana_Simplified.get_main_wallet_solana_balance(solana_client, destination_pubkey)
destination_token_balance = Solana_Simplified.get_token_account_balance(spl_client, destination_token_pubkey)

#send and check spl token from sender to destination
spl_token_transfer_transaction = Solana_Simplified.send_spl_token(spl_client, sender_token_pubkey, destination_token_pubkey, source_main_wallet_keypair, 1)
token_transaction_signature = Solana_Simplified.set_transaction_signature(spl_token_transfer_transaction)
time.sleep(20) #wait for transaction to process
check_token_transaction = Solana_Simplified.check_token_transaction(solana_client, token_transaction_signature)

#send and check solana from sender to destination
solana_transfer_transaction = Solana_Simplified.send_solana(solana_client, sender_pubkey, destination_pubkey, source_main_wallet_keypair, 0.001)
solana_transaction_signature = Solana_Simplified.set_transaction_signature(solana_transfer_transaction)
time.sleep(20) #wait for transaction to process
check_solana_transaction = Solana_Simplified.check_solana_transaction(solana_client, solana_transaction_signature)
#check_solana_transaction_direct = Solana_Simplified.check_solana_transaction_direct(solana_client, solana_transaction_signature) | Does not work for some reason

print(source_main_wallet_keypair)
print(sender_pubkey)
print(destination_pubkey)
print(program_pubkey)
print(token_address_pubkey)
print(solana_client)
print(spl_client)
print(sender_token_pubkey)
print(check_sender_token_account)
print(destination_token_pubkey)
print(check_destination_token_account)
print(sender_solana_balance)
print(sender_token_balance)
print(destination_solana_balance)
print(destination_token_balance)
print(spl_token_transfer_transaction)
print(token_transaction_signature)
print(check_token_transaction)
print(solana_transfer_transaction)
print(solana_transaction_signature)
print(check_solana_transaction)
#print(check_solana_transaction_direct)