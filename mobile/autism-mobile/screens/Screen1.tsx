import React, { useState, useEffect, } from "react";
import {
  View,
  TouchableOpacity,
  Text,
  StyleSheet,
  Alert,
  Image,
  ActivityIndicator
} from "react-native";

import { SafeAreaView, TextInput } from "react-native";
import Icon from "react-native-vector-icons/MaterialIcons";
import * as Speech from "expo-speech";

import CryptoJS from "crypto-js";

import axios from "axios";

// Local images stored in the assets folder
const localImages: { [key: string]: any } = {
  i: require("../assets/images/i.png"),
  is: require("../assets/images/is.png"),
  c: require("../assets/images/how.png"),
  have: require("../assets/images/have.png"),
  who: require("../assets/images/who.png"),
  f: require("../assets/images/where.png"),
  g: require("../assets/images/that.png"),
  can: require("../assets/images/can.png"),
  you: require("../assets/images/you.png"),
  pass: require("../assets/images/pass.png"),
  me: require("../assets/images/me.png"),
  water: require("../assets/images/water.png"),
  please: require("../assets/images/please.png"),
  get: require("../assets/images/get.png"),
  milk: require("../assets/images/milk.png"),
  from: require("../assets/images/from.png"),
  fridge: require("../assets/images/fridge.png"),
  make: require("../assets/images/make.png"),
  some: require("../assets/images/some.png"),
  juice: require("../assets/images/juice.png"),
  together: require("../assets/images/together.png"),
  love: require("../assets/images/love.png"),
  this: require("../assets/images/this.png"),
  cereal: require("../assets/images/cereal.png"),
  help: require("../assets/images/help.png"),
  with: require("../assets/images/with.png"),
  bread: require("../assets/images/bread.png"),
  butter: require("../assets/images/butter.png"),
  table: require("../assets/images/table.png"),
  like: require("../assets/images/like.png"),
  cheese: require("../assets/images/cheese.png"),
  my: require("../assets/images/my.png"),
  sandwich: require("../assets/images/sandwich.png"),
  apple: require("../assets/images/apple.png"),
  banana: require("../assets/images/banana.png"),
  ripe: require("../assets/images/ripe.png"),
  delicious: require("../assets/images/delicious.png"),
  time: require("../assets/images/time.png"),
  eat: require("../assets/images/eat.png"),
  dinner: require("../assets/images/dinner.png"),
  play: require("../assets/images/play.png"),
  game: require("../assets/images/game.png"),
  now: require("../assets/images/now.png"),
  we: require("../assets/images/we.png"),
  watch: require("../assets/images/watch.png"),
  movie: require("../assets/images/movie.png"),
  want: require("../assets/images/want.png"),
  read: require("../assets/images/read.png"),
  book: require("../assets/images/book.png"),
  listen: require("../assets/images/listen.png"),
  music: require("../assets/images/music.png"),
  would: require("../assets/images/would.png"),
  draw: require("../assets/images/draw.png"),
  picture: require("../assets/images/picture.png"),
  color: require("../assets/images/color.png"),
  go: require("../assets/images/go.png"),
  outside: require("../assets/images/outside.png"),
  and: require("../assets/images/and.png"),
  park: require("../assets/images/park.png"),
  ride: require("../assets/images/ride.png"),
  bike: require("../assets/images/bike.png"),
  today: require("../assets/images/today.png"),
  hide: require("../assets/images/hide.png"),
  seek: require("../assets/images/seek.png"),
  cook: require("../assets/images/cook.png"),
  clean: require("../assets/images/clean.png"),
  room: require("../assets/images/room.png"),
  need: require("../assets/images/need.png"),
  wash: require("../assets/images/wash.png"),
  hands: require("../assets/images/hands.png"),
  going: require("../assets/images/going.png"),
  brush: require("../assets/images/brush.png"),
  teeth: require("../assets/images/teeth.png"),
  take: require("../assets/images/take.png"),
  bath: require("../assets/images/bath.png"),
  dressed: require("../assets/images/dressed.png"),
  blue: require("../assets/images/blue.png"),
  shirt: require("../assets/images/shirt.png"),
  wearing: require("../assets/images/wearing.png"),
  red: require("../assets/images/red.png"),
  shoes: require("../assets/images/shoes.png"),
  jacket: require("../assets/images/jacket.png"),
  use: require("../assets/images/use.png"),
  computer: require("../assets/images/computer.png"),
  video: require("../assets/images/video.png"),
  hungry: require("../assets/images/hungry.png"),
  for: require("../assets/images/for.png"),
  snack: require("../assets/images/snack.png"),
  cookie: require("../assets/images/cookie.png"),
  cake: require("../assets/images/cake.png"),
  smells: require("../assets/images/smells.png"),
  amazing: require("../assets/images/amazing.png"),
  ice: require("../assets/images/ice.png"),
  cream: require("../assets/images/cream.png"),
  shopping: require("../assets/images/shopping.png"),
  weekend: require("../assets/images/weekend.png"),
  visit: require("../assets/images/visit.png"),
  grandma: require("../assets/images/grandma.png"),
  soon: require("../assets/images/soon.png"),
  talk: require("../assets/images/talk.png"),
  mom: require("../assets/images/mom.png"),
  speak: require("../assets/images/speak.png"),
  dad: require("../assets/images/dad.png"),
  goodnight: require("../assets/images/goodnight.png"),
  everyone: require("../assets/images/everyone.png"),
  bed: require("../assets/images/bed.png"),
  story: require("../assets/images/story.png"),
  sleep: require("../assets/images/sleep.png"),
  teddy: require("../assets/images/teddy.png"),
  bear: require("../assets/images/bear.png"),
  turn: require("../assets/images/turn.png"),
  off: require("../assets/images/off.png"),
  lights: require("../assets/images/lights.png"),
  open: require("../assets/images/open.png"),
  window: require("../assets/images/window.png"),
  dance: require("../assets/images/dance.png"),
  jump: require("../assets/images/jump.png"),
  swinging: require("../assets/images/swinging.png"),
  yard: require("../assets/images/yard.png"),
  slide: require("../assets/images/slide.png"),
  down: require("../assets/images/down.png"),
  sweep: require("../assets/images/sweep.png"),
  floor: require("../assets/images/floor.png"),
  laundry: require("../assets/images/laundry.png"),
  feed: require("../assets/images/feed.png"),
  pet: require("../assets/images/pet.png"),
  dog: require("../assets/images/dog.png"),
  walk: require("../assets/images/walk.png"),
  plants: require("../assets/images/plants.png"),
  plant: require("../assets/images/plant.png"),
  flowers: require("../assets/images/flowers.png"),
  garden: require("../assets/images/garden.png"),
  dishes: require("../assets/images/dishes.png"),
  set: require("../assets/images/set.png"),
  clear: require("../assets/images/clear.png"),
  popcorn: require("../assets/images/popcorn.png"),
  build: require("../assets/images/build.png"),
  blocks: require("../assets/images/blocks.png"),
  picnic: require("../assets/images/picnic.png"),
  dressup: require("../assets/images/dress-up.png"),
  puzzle: require("../assets/images/puzzle.png"),
  dolls: require("../assets/images/dolls.png"),
  tea: require("../assets/images/tea.png"),
  party: require("../assets/images/party.png"),
  fort: require("../assets/images/fort.png"),
  living: require("../assets/images/living.png"),
  funny: require("../assets/images/funny.png"),
  joke: require("../assets/images/joke.png"),
  tell: require("../assets/images/tell.png"),
  sing: require("../assets/images/sing.png"),
  song: require("../assets/images/song.png"),
  craft: require("../assets/images/craft.png"),
  project: require("../assets/images/project.png"),
  paint: require("../assets/images/paint.png"),
  favicon: require("../assets/images/favicon.png"),
  cookies: require("../assets/images/cookies.png"),
  catch: require("../assets/images/catch.png"),
  scooter: require("../assets/images/scooter.png"),
  soccer: require("../assets/images/soccer.png"),
  library: require("../assets/images/library.png"),
  tomorrow: require("../assets/images/tomorrow.png"),
  sleepover: require("../assets/images/sleepover.png"),
  stars: require("../assets/images/stars.png"),
  tonight: require("../assets/images/tonight.png"),
  scrapbook: require("../assets/images/scrapbook.png"),
  science: require("../assets/images/science.png"),
  experiment: require("../assets/images/experiment.png"),
  write: require("../assets/images/write.png"),
  letter: require("../assets/images/letter.png"),
  friend: require("../assets/images/friend.png"),
  school: require("../assets/images/school.png"),
  were: require("../assets/images/were.png"),
};

export default function Screen1() {
  const [text, onChangeText] = useState("Display Text");
  const [combinedText, setCombinedText] = useState("Display Text");
  const [selectedTexts, setSelectedTexts] = useState<string[]>([]);
  const [displayList, setDisplayList] = useState<string[]>([]);
  const [counter, setCounter] = useState(0);
  const [flag, setFlag] = useState(0);
  const [imageUrls, setImageUrls] = useState<
    { word: string; imageUrl: string | null }[]
  >([]);


  const imageCache: { [key: string]: string } = {};

  // generate the same id's for the string everytime.

  function generateId(inputString: string): string {
    return CryptoJS.MD5(inputString).toString(CryptoJS.enc.Hex);
  }

  useEffect(() => {
    fetchDisplayWords();
  }, [counter]);

  useEffect(() => {
    fetchImages();
  }, [displayList]);

  const fetchImages = async () => {
    try {
      const imageRequests = displayList.map(async (word) => {
        // Check if image is available locally
        if (localImages[word]) {
          return { word, imageUrl: localImages[word] };
        }

        // Check if image is already cached in memory
        if (imageCache[word]) {
          return { word, imageUrl: imageCache[word] };
        }
        const id = generateId(word);
        // console.log("this is the generated id", id);
        try {
          const response = await axios.get(
            `http://192.168.1.66:5000/api/images?query=${word}&id=${id}`
          );
          let imageUrl: string | null = "";
          // console.log("response",response.data);
          if (response.data.length > 0) {
            imageUrl = response.data;
          } else {
            imageUrl = response.data;
          }

          // console.log("this is the image url", imageUrl);
          // Cache the image URL in memory
          if (imageUrl) {
            imageCache[word] = imageUrl;
          }

          if (!imageUrl) {
            console.log("No image found for word:", word);
          }

          return { word, imageUrl };
        } catch (error) {
          console.error(`Failed to fetch image for word: ${word}`, error);
          return { word, imageUrl: null };
        }
      });

      const imageResults = await Promise.all(imageRequests);

      setImageUrls(imageResults);
      // console.log("yo sabai image haru fetch bhako ho", imageResults);
    } catch (error) {
      console.error("Failed to fetch images:", error);
    }
  };

  const fetchDisplayWords = async () => {
    try {
      const response = await fetch(
        ` http://192.168.1.66:5000/api/display_words?count=${counter}`
      );
      if (!response.ok) {
        throw new Error("Network response was not ok");
      }
      const data = await response.json();
      // console.log("Fetched words:", data);
      setDisplayList(data);
    } catch (error) {
      console.error("Failed to fetch:", error);
    }
  };

  const sendPostRequest = async (item: string, flag: Number) => {
    console.log("post garepaxi", item, flag);
    const url = `http://192.168.1.66:5000/api/guu`;
    const data = {
      item: item,
      flag: flag,
    };
    // console.log(data);
    try {
      const response = await fetch(url, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (response.ok) {
        const jsonResponse = await response.json();
        // console.log("Response:", jsonResponse);
        setDisplayList(jsonResponse);
        // console.log("Updated list:", displayList);
      } else {
        Alert.alert("Error", `Server Error: ${response.status}`);
      }
    } catch (error: any) {
      Alert.alert("Error", `Error sending data: ${error.message}`);
    }
  };

  console.log("this is display list haha", displayList);

  const speak = async (textToSpeak: string) => {
    try {
      await Speech.speak(textToSpeak);
    } catch (error) {
      console.error("Failed to speak:", error);
      Alert.alert("Error", "Failed to speak. Please try again.");
    }
  };

  const handleBoxPress = (item: string) => {
    console.log("Box pressed");
    sendPostRequest(item, flag);
    setSelectedTexts((prevSelectedTexts) => {
      const newSelectedTexts = [...prevSelectedTexts, item];
      const combinedText = newSelectedTexts.join(" ");
      onChangeText(combinedText);
      setCombinedText(combinedText);
      return newSelectedTexts;
    });
  };

  const handleTextChange = (newText: string) => {
    const newSelectedTexts = newText.split(" ").filter((item) => item !== "");
    setSelectedTexts(newSelectedTexts);
    onChangeText(newText);
  };

  const handleDeleteLastItem = () => {
    setSelectedTexts((prevSelectedTexts) => {
      const newSelectedTexts = prevSelectedTexts.slice(0, -1);
      const combinedText = newSelectedTexts.join(" ");
      onChangeText(combinedText);
      return newSelectedTexts;
    });
  };

  const handleCorrectItem = () => {
    setFlag(1);
    sendPostRequest("1", flag);
    speak(combinedText);
    handleTextChange("");
    // fetchDisplayWords()
  };

  const handleRefreshItem = () => {
    if (counter >= 3) {
      setCounter(0);
    } else {
      setCounter(counter + 1);
    }
  };

  return (
    <View style={styles.container}>
      <SafeAreaView>
        <View style={styles.inputContainer}>
          <TextInput
            style={styles.input}
            value={text}
            onChangeText={handleTextChange}
            editable={false}
          />
          <TouchableOpacity
            onPress={handleRefreshItem}
            style={styles.refreshContainer}
          >
            <Icon name="refresh" size={26} color="white" />
          </TouchableOpacity>
        </View>
      </SafeAreaView>
      <View style={styles.boxContainer}>
        {displayList.map((item, index) => {
          const imageUrl = imageUrls.find((img) => img.word === item)?.imageUrl;
          return (
            <View key={index}>
              <TouchableOpacity
                style={[styles.box, { backgroundColor: "" }]}
                onPress={() => handleBoxPress(item)}
              >
                {localImages[item] ? (
                  <Image
                    source={localImages[item]}
                    style={[styles.box]}
                    progressiveRenderingEnabled={true}
                    resizeMode="cover"
                  />
                ) : imageUrl ? (
                  <Image
                    source={{ uri: imageUrl }}
                    style={[styles.box]}
                    progressiveRenderingEnabled={true}
                    resizeMode="cover"
                  />
                ) : (
                  <></>
                )}
              </TouchableOpacity>
              <Text style={styles.boxTextBelow}>{item}</Text>
            </View>
          );
        })}
      </View>

      <View style={styles.lowerContainer}>
        <TouchableOpacity
          onPress={handleDeleteLastItem}
          style={styles.closeIconContainer}
        >
          <Icon name="close" size={28} color="white" />
        </TouchableOpacity>
        <TouchableOpacity
          onPress={handleCorrectItem}
          style={styles.correctIconContainer}
        >
          <Icon name="check" size={28} color="white" />
        </TouchableOpacity>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: "center",
    alignItems: "center",
    marginBottom: 100,
  },
  boxContainer: {
    flexDirection: "row",
    flexWrap: "wrap",
    justifyContent: "center",
    alignItems: "center",
    width: 400,
    marginTop: 10,
  },
  box: {
    borderRadius: 30,
    width: 100,
    height: 100,
    justifyContent: "center",
    alignItems: "center",
    margin: 10,
    transitionProperty:"ease-in-out"
  },
  boxText: {
    color: "#ffffff",
    fontSize: 20,
  },
  input: {
    height: 40,
    width: 280,
    margin: 12,
    padding: 10,
  },

  boxTextBelow: {
    color: "#000",
    fontSize: 18,
    marginTop: 5,
    textAlign: "center",
    alignSelf: "center",
  },
  inputContainer: {
    flexDirection: "row",
    alignItems: "center",
    right: 10,
    width: 320,
    height: 50,
    borderColor: "gray",
    borderWidth: 1,
    marginTop: 30,
  },
  closeIconContainer: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "rgb(28,150,65)",
    height: 50,
    width: 165,
  },
  correctIconContainer: {
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    backgroundColor: "rgb(0,119,255)",
    height: 50,
    width: 165,
  },

  refreshContainer: {
    flexDirection: "row",
    justifyContent: "center",
    alignItems: "center",
    backgroundColor: "black",
    height: 50,
    width: 38,
    left: 2,
  },

  lowerContainer: {
    top: 20,
    flexDirection: "row",
    justifyContent: "center",
    alignContent: "center",
    gap: 10,
  },
});
