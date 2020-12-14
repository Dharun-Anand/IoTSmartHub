package com.example.iothomesystem

import android.graphics.Color
import android.os.Bundle
import androidx.appcompat.app.AppCompatActivity
import com.google.firebase.database.*
import com.google.firebase.database.ktx.database
import com.google.firebase.ktx.Firebase
import kotlinx.android.synthetic.main.activity_main.*


class MainActivity : AppCompatActivity() {
    lateinit var database: DatabaseReference

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        //setSupportActionBar(toolbar)

        database = Firebase.database.reference

        database.child("IoTHomeSystem1").child("System").addValueEventListener(object : ValueEventListener{ //find system status
            override fun onCancelled(error: DatabaseError) { }
            override fun onDataChange(snapshot: DataSnapshot) {
                if (snapshot.value.toString() == "ON") { //if system status is on
                    system.setChecked(true) //turn system switch on

                    system.setOnClickListener {
                        database.child("IoTHomeSystem1").child("System").setValue("OFF") //if system switch toggled, toggle system status
                    }

                    lights.setEnabled(true) //enable operation of lights
                    database.child("IoTHomeSystem1").child("Lights").addValueEventListener(object : ValueEventListener{ //get lights status
                        override fun onCancelled(error: DatabaseError) { }
                        override fun onDataChange(snapshot: DataSnapshot) {
                            if (snapshot.value.toString() == "ON") { //if light status is on
                                lights.setChecked(true) //turn light switch on
                                lights.setOnClickListener {
                                    database.child("IoTHomeSystem1").child("Lights").setValue("OFF")  //if lights switch toggled, toggle lights status
                                }
                            }
                            if (snapshot.value.toString() == "OFF") { //if light status is off
                                lights.setChecked(false) //turn light switch off
                                lights.setOnClickListener {
                                    database.child("IoTHomeSystem1").child("Lights").setValue("ON")  //if lights switch toggled, toggle lights status
                                }
                            }
                        }
                    })
                    motion.setEnabled(true) //enable operation of motion
                    database.child("IoTHomeSystem1").child("Motion").addValueEventListener(object : ValueEventListener{ //get motion status
                        override fun onCancelled(error: DatabaseError) { }
                        override fun onDataChange(snapshot: DataSnapshot) {
                            if (snapshot.value.toString() == "OFF") { //if motion status is off
                                motion.text = "No Motion Detected"
                                motion.setTextColor(Color.parseColor("#2bfe72"))
                            }
                            if (snapshot.value.toString() == "ON") { //if motion status is on
                                motion.text = "Motion Detected!!!"
                                motion.setTextColor(Color.parseColor("#f6546a"))
                            }
                        }
                    })

                    tempView.setEnabled(true) //enable operation of temperature
                    database.child("IoTHomeSystem1").child("TH").child("Temp").addValueEventListener(object : ValueEventListener{ //get temperature
                        override fun onCancelled(error: DatabaseError) { }
                        override fun onDataChange(snapshot: DataSnapshot) {
                            tempView.text = "Temperature [C] : " + snapshot.value.toString()
                        }
                    })

                    humidView.setEnabled(true) //enable operation of humidity
                    database.child("IoTHomeSystem1").child("TH").child("Humid").addValueEventListener(object : ValueEventListener{ //get humidity
                        override fun onCancelled(error: DatabaseError) { }
                        override fun onDataChange(snapshot: DataSnapshot) {
                            humidView.text = "Humidity [%] : " + snapshot.value.toString()
                        }
                    })
                }
                if (snapshot.value.toString() == "OFF") { //if system status is off
                    system.setChecked(false) //turn system switch off

                    system.setOnClickListener {
                        database.child("IoTHomeSystem1").child("System").setValue("ON")  //if system switch toggled, toggle system status
                    }

                    humidView.setEnabled(false)
                    tempView.setEnabled(false)
                    lights.setEnabled(false)
                    motion.setEnabled(false)
                }
            }
        })
    }
}