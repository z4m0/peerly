# P2P stuff indexer
Peerly is a P2P stuff indexer, that means that is a highly distributed database indexed by keywords (or tags). You can store something (up to 8KB) in the DB and retrieve later inserting some of the tags you used before.

##Installation

Install first [peerlyDB](https://github.com/z4m0/peerlyDB)

Download, unzip and uncompress the project
```
sudo python setup.py install
```

##Usage

In a console type:
```
peerly
```

Open the browser and go to:
```
http://localhost:8080
```

##Connect to Peerly network
To connect to the Peerly you must know an entry point (i.e. the IP and port of somebody already in the network). After a successful connect you will see your ip and port in the top right corner and you can start inviting your friends!

##Insert stuff in Peerly
When you insert something to the DB you will we asked a title, url, description (optional) and some tags. The tags are the words that your file will be indexed. You can add up to 16 tags.

##Search stuff in Peerly
Just insert the search tags and press search!

##How it works?
Peerly is based on Kademlia. Kademlia is a Distributed Hash Table (DHT) that means each peer has a piece of the DB. 
Each pair tag, value is transalted to a hash and stored to some peers. If a peer disconnects from the network the entry won't disapear as it is stored to other peers. Each key can contain up to 50 values. That means if you put something indexed with the word "home" and somebody adds something else with the same tag your entry won't disappear. And both entries will appear as results in the search. But if 50 people insert something with the tag "home" your entry finally disapears. So, this DB tends to forget.

##Contribute
Please fork this repository and contribute!! With new ideas too!

##How to develop or start your own network
TODO

##What is done so far
* Search for a key and get the results.
* Insert new values to the DB

##TODO
This is a list of things in the roadmap. Don't know if I will implement all of them yet:

* Allow the users comment. Each hash(value) can be the comments thread.

* Voting system: Each user can vote up or vote down an entry. The most voted entries should remain more time. The user can see what the comunity things about this entry. The votes won't be stored in the same location as the value. This means that the kademlia protocol should be extended.

* Clean the code which is ugly and hacky.



