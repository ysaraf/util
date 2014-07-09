import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

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
    Map<String, Set<String>> encodingsToTokens = new HashMap<String, Set<String>>();
    BufferedReader br = new BufferedReader(new FileReader(filename));
    String line;
    while ((line = br.readLine()) != null) {
      String[] parts = line.split("\t");
      String query =  parts[0];
      if (query == null || query.isEmpty()) {
        continue;
      }
      query = URLDecoder.decode(query, StandardCharsets.UTF_8.name());
      query = query.replaceAll("\"", "");
      String[] tokens = query.split(" ");
      for (String token : tokens) {
        if (token.length() < 2) {
          continue;
        }
        String encoding = doubleMetaphone.doubleMetaphone(token);
        if (encoding == null || encoding.isEmpty()) {
          continue;
        }
        Set<String> currentTokens = encodingsToTokens.get(encoding);
        if (currentTokens == null) {
          currentTokens = new HashSet<String>();
          encodingsToTokens.put(encoding, currentTokens);
        }
        currentTokens.add(token);
      }
    }
    br.close();

    for (Map.Entry<String, Set<String>> entry : encodingsToTokens.entrySet()) {
      StringBuilder sb = new StringBuilder(entry.getKey());
      for (String token : entry.getValue()) {
        sb.append("\t").append(token);
      }
      System.out.println(sb.toString());
    }
  }
}
