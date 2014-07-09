import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.apache.commons.codec.language.DoubleMetaphone;

public class PhoneticConverterTool {

  public static void main(String[] args) throws IOException {
    if (args.length < 1) {
      System.out.println("Filename is required");
      System.exit(1);
    }

    DoubleMetaphone doubleMetaphone = new DoubleMetaphone();
    doubleMetaphone.setMaxCodeLen(6);

    String filename = args[0];
    Map<String, List<String>> encodingsToTokens = new HashMap<String, List<String>>();
    BufferedReader br = new BufferedReader(new FileReader(filename));
    String line;
    while ((line = br.readLine()) != null) {
      String[] parts = line.split("\t");
      String query =  parts[0];
      String[] tokens = query.split(" ");
      for (String token : tokens) {
        String encoding = doubleMetaphone.doubleMetaphone(token);
        //System.out.println(query + "\t" + encoding);
        List<String> list = encodingsToTokens.get(encoding);
        if (list == null) {
          list = new ArrayList<String>();
          encodingsToTokens.put(encoding, list);
        }
        list.add(token);
      }
    }
    br.close();

    System.out.println("Encodings -> Tokens");
    for (Map.Entry<String, List<String>> entry : encodingsToTokens.entrySet()) {
      if (entry.getValue().size() < 2) {
        continue;
      }
      System.out.println(entry.getKey() + "\t" + entry.getValue());
    }
  }
}
