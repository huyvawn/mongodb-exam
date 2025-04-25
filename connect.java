import com.mongodb.client.*;
import org.bson.Document;

public class MongoConnection {
    public static MongoDatabase connect() {
        MongoClient mongoClient = MongoClients.create("mongodb://localhost:27017");
        return mongoClient.getDatabase("eShop");
    }
}