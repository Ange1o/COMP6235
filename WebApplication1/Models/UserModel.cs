
using System;
using System.Collections.Generic;
using System.Linq;
using System.Web;
using System.ComponentModel.DataAnnotations;
using System.Web.Mvc;
using MongoDB.Bson;
using MongoDB.Driver;
using MongoDB.Driver.Core;
using MongoDB.Driver.Linq;
using MongoDB.Bson.Serialization.Attributes;

namespace MvcApplication1.Models
{


    public class t
        {
        public ObjectId _id { get; set; }
        public string Year{ get; set; }
        public string query_result_title { get; set; }
        public string Month { get; set; }
        public string query_result_link { get; set; }
        public string rising { get; set; }
        //[BsonDateTimeOptions]
        public string Date { get; set; }
        public string keyword { get; set; }
        public string query_result_des { get; set; }

        //public string query_result_content { get; set; }
       
        public string top_query_id { get; set; }




    }
}
 
