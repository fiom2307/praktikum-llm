// Mascot outfits
import defaultMascot from "../assets/outfits/hello.png"; 
import darthVaderImg from "../assets/outfits/darthVader.png";
import gladiatorImg from "../assets/outfits/gladiator.png";
import chefImg from "../assets/outfits/chef.png";          
import godfatherImg from "../assets/outfits/godfather.png"; 
import maradonaImg from "../assets/outfits/maradona.png";   
import ferrariImg from "../assets/outfits/ferrari.png";   

const COSTUME_MAP = {
    0: defaultMascot,
    1: darthVaderImg,
    2: gladiatorImg,
    3: chefImg,
    4: godfatherImg,
    5: maradonaImg,
    6: ferrariImg
};

export default function Mascot({ costumeId = 0, ...props }) {
    const currentMascotImg = COSTUME_MAP[costumeId] || defaultMascot;

    return <img src={currentMascotImg} alt="Mascot" {...props} />;
}
