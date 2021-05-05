//
//  ViewController.swift
//  Phone Toss
//

import UIKit
import CoreMotion
import AVFoundation

class ViewController: UIViewController {

    var reading = false
    let threshold = Float(0.2)
    var secs = 0.0
    var window = Array(repeating: 0.0, count: 20)
    var updatesSinceStart = 0
    @IBOutlet weak var hangtime: UILabel!
    @IBOutlet weak var accel: UILabel!
    @IBOutlet weak var startButton: UIButton!
    let motionManager = CMMotionManager()
    var audioPlayer = AVAudioPlayer()
    
    override func viewDidLoad() {
        super.viewDidLoad()
        accel.text = "0"
        hangtime.text = "0.00s"
        // Do any additional setup after loading the view.
        let sound = Bundle.main.path(forResource: "supershort", ofType: "mp3")

        do{
            audioPlayer = try AVAudioPlayer(contentsOf: URL(fileURLWithPath: sound!))
        }
        catch{
            print(error)
        }
    }

    @IBAction func buttonPressed(_ sender: UIButton){
        if motionManager.isAccelerometerAvailable {
            updatesSinceStart = 0
            if(reading == false){
                motionManager.accelerometerUpdateInterval = 0.01
                motionManager.startAccelerometerUpdates(to: OperationQueue.main) {
                    (data, error) in self.process(input: data!)}
                reading = true
            }
        }
        else{
            motionManager.stopAccelerometerUpdates()
            reading = false
        }
    }
    
    func process(input: CMAccelerometerData){
        //with each new accelerometer update
        //calculate it's magnitude
        let x = input.acceleration.x
        let y = input.acceleration.y
        let z = input.acceleration.z
        let net = sqrt(x*x + y*y + z*z)
        //add magnitude to queue recent readings
        //if fewer than 20 recent readings (.2 seconds), let it fill up.
        if(updatesSinceStart < 20){
            window.append(net)
        }
        //else, start dequeueing to keep a moving window of the last 20 readings.
        else{
            let newArray = window.dropFirst(1)
            for n in 0...18 {
                window[n] = newArray[n]
            }
            window[19] = net
            //set accel label to the mean of the last 20 readings.
            var sum = 0.0
            for value in window{
                sum += value
            }
            //rounded to 3 decimals
            let roundedSum = Float(round(1000*(sum/20))/1000)
            accel.text = "\(roundedSum)"
            if (roundedSum <= threshold){
                secs += 0.01
                if(secs <= 0.1 && (Int(secs * 100)) % 10 == 0){
                    //play scream sound
                    audioPlayer.play()
                }
            }
        }
    }
}

