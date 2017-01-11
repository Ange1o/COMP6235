using System;
using System.Collections.Generic;
using System.Xml.Linq;
using System.Linq;
using System.Web;
using System.Web.Mvc;
using MvcApplication1.Models;
using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Driver.Core;
using MongoDB.Driver.Linq;
using System.Collections;
using System.Configuration;
using System.Globalization;

namespace WebApplication1.Controllers
{
    public class userController : Controller
    {
        private MongoDatabase database;


        public userController()
        {

            var connectionstring = "mongodb://localhost";
            var client = new MongoClient(connectionstring);

            var server = client.GetServer();

            database = server.GetDatabase("trends");
            int a = 1;


        }

      
       
        public JsonResult GetAll()
        {

            var collections = database.GetCollection<t>("beef_trend");
            IList<t> jsonResult = new List<t>();
            var gett = collections.FindAs(typeof(t), MongoDB.Driver.Builders.Query.EQ("rising", "1.1"));
            foreach (t item in gett)
            {
                jsonResult.Add(item);
                Console.WriteLine(item);
            }
                
            return Json(jsonResult, JsonRequestBehavior.AllowGet);
        }

        public JsonResult Get(string c)
        {
            //DateTime da,bb;

            //da = Convert.ToDateTime(a);
            //bb = Convert.ToDateTime(b);
            //Console.WriteLine(da);
            //var collections = database.GetCollection<t>("beef_trend");
            var collections = database.GetCollection<t>(c);
            IList<t> jsonResult = new List<t>();
            
            /* var filterBuilder = Builders<t>.Filter;
             var filter = filterBuilder.Gte("Date", a) &
                           filterBuilder.Lte("Date", b);

                 jsonResult = collections.Find(filter).ToList();*/
           
            var gett = collections.FindAs(typeof(t), MongoDB.Driver.Builders.Query.NE("rising", "-1"));
            // var gett = collections.FindAs(typeof(t), MongoDB.Driver.Builders.Query.And(MongoDB.Driver.Builders.Query.GTE("Date",a),MongoDB.Driver.Builders.Query.LTE("Date", b)));
            foreach (t item in gett)
            {
                jsonResult.Add(item);
                Console.WriteLine(item);
            }

            return Json(jsonResult, JsonRequestBehavior.AllowGet);
        }

        public JsonResult search(string a)
        {

            var collections = database.GetCollection<t>("beef_trend");
            IList<t> jsonResult = new List<t>();
            var gett = collections.FindAs(typeof(t), MongoDB.Driver.Builders.Query.EQ("rising", "1.1"));
            foreach (t item in gett)
            {
                jsonResult.Add(item);
                Console.WriteLine(item);
            }

            return Json(jsonResult, JsonRequestBehavior.AllowGet);
        }

     

        public ActionResult indexView()
        {

           /* var collections = database.GetCollection<t>("beef_trend");
            IList<t> jsonResult = new List<t>();
            var gett = collections.FindAs(typeof(t), MongoDB.Driver.Builders.Query.NE("keyword", "null"));
            foreach (t item in gett)
            {
                jsonResult.Add(item);
            }
            */
            //(jsonResult, JsonRequestBehavior.AllowGet);
            return View();

        }

        // GET: user
        public ActionResult Index()
        {
           
            return View();
            
        }
       


        /*public ActionResult GetUsers()
        {
            var connectionstring = "mongodb://localhost";
            var client = new MongoClient(connectionstring);
            var server = client.GetServer();
            database= server.GetDatabase("football");
          
            
          
            MongoClient client = new MongoClient(ConfigurationManager.AppSettings["Server=localhost:27017"]);
            MongoServer objServer = client.GetServer();
            MongoDatabase objDatabse = objServer.GetDatabase("MVCTestDB");
            IList UserDetails = objDatabse.GetCollection("Users").FindAll().ToList();
            return View(UserDetails);
          
            
        }
    
        public ActionResult select(int id)
        {
          MongoClient client = new MongoClient(ConfigurationManager.AppSettings["Server=localhost:27017"]);
            MongoServer objServer = client.GetServer();
            MongoDatabase objDatabse = objServer.GetDatabase("MVCTestDB");
            IMongoQuery query = MongoDB.Driver.Builders.Query.EQ("ID", id);
            var user=Json(objDatabse.GetCollection("Users").Find(query).SingleOrDefault());
            ViewData["user"] = user;
            
            return View();
        }
       */

        public ActionResult test() {
            return View();
        }
    }
}