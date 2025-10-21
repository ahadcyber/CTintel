"""
MongoDB connection manager for CTI Dashboard
"""
import os
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class MongoDBManager:
    """Manages MongoDB connection and operations"""
    
    def __init__(self):
        try:
            mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/')
            # Add SSL parameters for MongoDB Atlas
            self.client = MongoClient(
                mongo_uri, 
                serverSelectionTimeoutMS=5000,
                tlsAllowInvalidCertificates=True,
                retryWrites=True
            )
        except Exception as e:
            print(f"Error initializing MongoDB client: {e}")
            self.client = None
        self.db = None
        self.collection = None
        
    def connect(self):
        """Establish connection to MongoDB"""
        try:
            # Test connection
            self.client.admin.command('ping')
            self.db = self.client['cti_dashboard']
            self.collection = self.db['iocs']
            
            # Create indexes for better performance
            self.collection.create_index([('value', ASCENDING)])
            self.collection.create_index([('type', ASCENDING)])
            self.collection.create_index([('source', ASCENDING)])
            self.collection.create_index([('timestamp', DESCENDING)])
            self.collection.create_index([('tags', ASCENDING)])
            
            print("✅ Connected to MongoDB successfully")
            return True
        except ConnectionFailure as e:
            print(f"❌ Failed to connect to MongoDB: {e}")
            return False
    
    def insert_ioc(self, ioc_data):
        """Insert a single IOC"""
        try:
            # Check if IOC already exists
            existing = self.collection.find_one({'value': ioc_data['value'], 'source': ioc_data['source']})
            if not existing:
                self.collection.insert_one(ioc_data)
                return True
            return False
        except Exception as e:
            print(f"Error inserting IOC: {e}")
            return False
    
    def insert_many_iocs(self, ioc_list):
        """Insert multiple IOCs"""
        if not ioc_list:
            return 0
        
        inserted = 0
        for ioc in ioc_list:
            if self.insert_ioc(ioc):
                inserted += 1
        return inserted
    
    def get_all_iocs(self, limit=100):
        """Retrieve all IOCs with limit"""
        try:
            return list(self.collection.find().sort('timestamp', DESCENDING).limit(limit))
        except Exception as e:
            print(f"Error retrieving IOCs: {e}")
            return []
    
    def search_iocs(self, query):
        """Search IOCs by value"""
        try:
            regex_query = {'value': {'$regex': query, '$options': 'i'}}
            return list(self.collection.find(regex_query).limit(50))
        except Exception as e:
            print(f"Error searching IOCs: {e}")
            return []
    
    def get_stats(self):
        """Get statistics about IOCs"""
        try:
            total_count = self.collection.count_documents({})
            
            # Count by type
            type_pipeline = [
                {'$group': {'_id': '$type', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            by_type = list(self.collection.aggregate(type_pipeline))
            
            # Count by source
            source_pipeline = [
                {'$group': {'_id': '$source', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            by_source = list(self.collection.aggregate(source_pipeline))
            
            return {
                'total': total_count,
                'by_type': by_type,
                'by_source': by_source
            }
        except Exception as e:
            print(f"Error getting stats: {e}")
            return {'total': 0, 'by_type': [], 'by_source': []}
    
    def add_tag_to_ioc(self, ioc_id, tag):
        """Add a tag to an IOC"""
        try:
            from bson.objectid import ObjectId
            result = self.collection.update_one(
                {'_id': ObjectId(ioc_id)},
                {'$addToSet': {'tags': tag}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error adding tag: {e}")
            return False
    
    def remove_tag_from_ioc(self, ioc_id, tag):
        """Remove a tag from an IOC"""
        try:
            from bson.objectid import ObjectId
            result = self.collection.update_one(
                {'_id': ObjectId(ioc_id)},
                {'$pull': {'tags': tag}}
            )
            return result.modified_count > 0
        except Exception as e:
            print(f"Error removing tag: {e}")
            return False
    
    def get_iocs_by_tag(self, tag):
        """Get all IOCs with a specific tag"""
        try:
            return list(self.collection.find({'tags': tag}).sort('timestamp', DESCENDING))
        except Exception as e:
            print(f"Error getting IOCs by tag: {e}")
            return []
    
    def get_trends(self, days=7):
        """Get IOC trends over time"""
        try:
            from datetime import datetime, timedelta
            
            start_date = datetime.utcnow() - timedelta(days=days)
            
            pipeline = [
                {'$match': {'timestamp': {'$gte': start_date}}},
                {'$group': {
                    '_id': {
                        'date': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$timestamp'}},
                        'type': '$type'
                    },
                    'count': {'$sum': 1}
                }},
                {'$sort': {'_id.date': 1}}
            ]
            
            results = list(self.collection.aggregate(pipeline))
            
            # Format results for charting
            trends = {}
            for item in results:
                date = item['_id']['date']
                ioc_type = item['_id']['type']
                count = item['count']
                
                if date not in trends:
                    trends[date] = {}
                trends[date][ioc_type] = count
            
            return trends
        except Exception as e:
            print(f"Error getting trends: {e}")
            return {}
    
    def get_threat_level_stats(self):
        """Get statistics by threat level"""
        try:
            pipeline = [
                {'$match': {'threat_level': {'$exists': True}}},
                {'$group': {'_id': '$threat_level', 'count': {'$sum': 1}}},
                {'$sort': {'count': -1}}
            ]
            return list(self.collection.aggregate(pipeline))
        except Exception as e:
            print(f"Error getting threat level stats: {e}")
            return []
    
    def close(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()
            print("✅ MongoDB connection closed")

# Singleton instance
db_manager = MongoDBManager()
